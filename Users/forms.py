# _*_ coding: utf-8 _*_
__author__ = 'willxin'
__date__ = '2017/8/14  19:59'

from django import forms
from .models import UserInfo
from captcha.fields import CaptchaField


# 表单验证类，继承django
class LoginForm(forms.Form):
    username = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=8)


class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True, min_length=8)
    password2 = forms.CharField(required=True, min_length=8)
    check_box = forms.BooleanField(required=True)
    # captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})

    # class Meta:
    #     model = UserInfo
    #     fields = ['username','email','password']
    #
    # def clean_password(self):
    #     password1 = forms.CharField(required=True, min_length=8)
    #     password2 = forms.CharField(required=True, min_length=8)
    #     mobile = self.cleaned_data['password1']
    #     REGEX_MOBILE = "(^1[358]\d{9}$)|(^147\d{8}$)|(^176\d{8}$)"
    #     p = re.compile(REGEX_MOBILE)
    #     if p.match(mobile):
    #         return mobile
    #     else:
    #         raise forms.ValidationError(u"手机号码非法",code='mobile_invalide')


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=8)
    password2 = forms.CharField(required=True, min_length=8)
