# coding=utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from utils import music

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from .models import UserInfo, EmailVerifyRecord
from utils.email_send import send_register_email

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from utils.mixin_utils import LoginRequiredMixin

from django.contrib.auth.models import Group


# Create your views here.


class MusicView(View):
    def get(self, request):
        return render(request, 'music.html', {})

    def post(self, request):
        list_id = request.POST.get('list_id', None)
        if list_id:
            return HttpResponseRedirect(reverse("users:song_music", kwargs={'list_id': list_id}))


class SongView(View):
    def get(self, request, list_id):
        result_dic = {}
        if list_id > 0:
            result_dic = music.get_song_list(list_id)
        return render(request, 'song.html', {
            'result_dic': result_dic.values()[:-1],
        })


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        # 数据库之前做form验证
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            # 自定义用户名的验证
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('user_index', kwargs={'uid': user.id}))
                else:
                    return render(request, "login.html", {
                        "msg": "邮箱 " + user_name + " 未激活",
                        "status": "block",
                        "user_email": user_name
                    })
            else:
                return render(request, "login.html", {"msg": "邮箱或密码错误", "status": "block", "user_email": user_name})
        else:
            return render(request, "login.html", {"msg": "邮箱或密码错误", "status": "block"})


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html", {})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return render(request, "register.html", {
                    "register_form": register_form,
                    "msg": u"密码输入不一致",
                    "status": "block"
                })
            else:
                email_account = request.POST.get("email", "")
                if UserInfo.objects.filter(email=email_account):
                    return render(request, "register.html", {
                        "register_form": register_form,
                        "msg": "邮箱 " + email_account + " 已注册",
                        "status": "block"
                    })
                pass_word = request.POST.get("password1", "")
                user_profile = UserInfo()
                user_profile.username = request.POST.get("username", "")
                user_profile.email = email_account
                user_profile.is_active = False
                user_profile.password = make_password(pass_word)
                user_profile.save()

                send_register_email.delay(email_account, "register")
                return render(request, "active_success.html", {
                    "title": "注册操作提示",
                    "msg": "邮件已发送到您的邮箱，请尽快激活"
                })
        else:
            return render(request, "register.html", {
                "register_form": register_form,
                "msg": u"邮箱格式出错或密码长度有误",
                "status": "block"
            })


class LogoutView(View):
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))


class ManageView(LoginRequiredMixin, View):
    def get(self, request):
        return render_to_response('toXadmin.html')


class ForgetPwdView(View):
    def get(self, request):
        # forget_form = ForgetForm()
        hashkey = CaptchaStore.generate_key()
        imgage_url = captcha_image_url(hashkey)
        return render(request, "forget.html", {
            "hashkey": hashkey,
            "imgage_url": imgage_url
        })

    def post(self, request):
        hashkey = CaptchaStore.generate_key()
        imgage_url = captcha_image_url(hashkey)
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email_account = request.POST.get("email", "")
            if UserInfo.objects.filter(email=email_account):

                send_register_email.delay(email_account, "forget")
                return render(request, "active_success.html", {
                    "title": "重置操作",
                    "msg": "邮件已发送到您的邮箱"
                })
            else:
                return render(request, "forget.html", {
                    "hashkey": hashkey, "imgage_url": imgage_url,
                    "status": "block",
                    "msg": "邮箱 " + email_account + " 未注册",
                })
        else:
            return render(request, "forget.html", {
                "hashkey": hashkey, "imgage_url": imgage_url,
                "status": "block",
                "msg": "请检查邮箱格式和验证码",
                "forget_form": forget_form
            })


# 与code有关,用get方法读取URL中的code
class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserInfo.objects.get(email=email)
                if user.is_active is False:
                    user.is_active = True
                    user.is_staff = True
                    group_per = Group.objects.get(name=u"普通用户")
                    user.groups.add(group_per)
                    user.save()
                    return render(request, "active_success.html", {
                        "title": "激活操作提示",
                        "msg": "邮箱激活完成，现在可以登陆"
                    })
                else:
                    return render(request, "active_fail.html", {
                        "title": "激活失败提示",
                        "msg": "链接已激活"
                    })
        else:
            return render(request, "active_fail.html", {
                "title": "激活失败提示",
                "msg": "无效的链接"
            })


# 与code有关,用get方法读取URL中的code
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserInfo.objects.get(email=email)
                if user.is_active is True:
                    return render(request, "reset.html", {"email": ' ' + email + ' '})
                else:
                    return render(request, "active_fail.html", {
                        "title": "操作失败提示",
                        "msg": "用户 " + email + " 未激活"
                    })
        else:
            return render(request, "active_fail.html", {
                "title": "访问失败提示",
                "msg": "无效的链接"
            })

    def post(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            register_form = ModifyPwdForm(request.POST)
            if register_form.is_valid():
                pwd1 = request.POST.get("password1", "")
                pwd2 = request.POST.get("password2", "")
                if pwd1 != pwd2:
                    return render(request, "reset.html", {
                        "msg": u"密码输入不一致",
                        "status": "block"
                    })
                else:
                    for record in all_records:
                        email = record.email
                        user = UserInfo.objects.get(email=email)
                        if user.is_active is True:
                            user.password = make_password(pwd1)
                            user.save()
                            return render(request, "active_success.html", {
                                "title": "重置操作提示",
                                "msg": "密码修改成功，请用新密码登录"
                            })
                        else:
                            return render(request, "active_fail.html", {
                                "title": "重置密码失败",
                                "msg": "用户 " + email + " 还未激活"
                            })
            else:
                return render(request, "reset.html", {
                    "msg": u"密码太弱不够8位",
                    "status": "block"
                })


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserInfo.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
