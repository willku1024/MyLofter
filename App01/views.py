# coding=utf8


from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.cache import cache

import json
from .models import LofterModel
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from Users.models import Comments
from utils.ip2pos import get_ip_pos
from utils.new_ip import generate_new_ip

# Create your views here.

class IndexView(View):
    def get(self, request):
        search_keywords = request.GET.get('keywords', '')

        if search_keywords:
            all_items = LofterModel.objects.filter(
                Q(title__icontains=search_keywords) | Q(content__icontains=search_keywords))
        else:
            all_items = LofterModel.objects.all()

        paginator = Paginator(all_items, 3)  # Show [num] contacts per page
        page = request.GET.get('page', '1')
        try:
            contacts = paginator.page(page)

            # 从缓存中取点赞数
            for contact in contacts:
                fav_nums = cache.get('fav_item_id_' + str(contact.id), None)
                # 存在
                if fav_nums is not None:
                    contact.fav_click = fav_nums

        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)

        return render(request, 'index.html', {
            'contacts': contacts,
        })


class AddFavView(View):
    def post(self, request):
        item_id = request.POST.get('item_id', '')
        if item_id:

            fav_nums = cache.get('fav_item_id_' + item_id, None)
            # 过期或值不存在
            if fav_nums is None:
                exist_records = LofterModel.objects.filter(id=int(item_id))[0]
                fav_nums = exist_records.fav_click
                cache.set('fav_item_id_' + item_id, int(fav_nums) ,None)


            has_clicked = request.session.get(item_id + '_clicked', False)
            if fav_nums and has_clicked is False:
                cache.incr('fav_item_id_' + item_id)
                request.session[item_id + '_clicked'] = True

            if fav_nums and has_clicked is True:
                if fav_nums > 0:
                    cache.decr('fav_item_id_' + item_id)
                request.session[item_id + '_clicked'] = False

            fav_nums = cache.get('fav_item_id_' + item_id)
            return JsonResponse({'status':'success','newfav':fav_nums})


class PerBlogView(View):
    def get(self, request, blog_id):
        blog_id = int(blog_id)
        blog_item = LofterModel.objects.filter(id=blog_id)[0]
        # SELECT `App01_loftermodel`.`id` FROM `App01_loftermodel`
        blog_list = LofterModel.objects.all().defer('title', 'timestamp', 'content', 'image',
                                                    'fav_click', 'author_id').values_list('id', flat=True)
        blog_list = list(blog_list)


        # 从缓存中取点赞数
        fav_nums = cache.get('fav_item_id_' + str(blog_item.id), None)
        # 存在
        if fav_nums is not None:
            blog_item.fav_click = fav_nums

        try:
            cur_pos = blog_list.index(blog_item.id)
        except:
            return render(request, 'active_fail.html', {'title': '404', 'msg': '访问页面不存在'})

        pre_pos = cur_pos - 1 if cur_pos != 0 else cur_pos
        next_pos = cur_pos + 1 if cur_pos != len(blog_list) - 1 else 0

        comments = Comments.objects.filter(essay=blog_id).order_by('-add_time')[:10]
        comments_count = Comments.objects.filter(essay=blog_id).count()
        if blog_item:
            return render(request, 'per_blog.html', {
                'blog_item': blog_item,
                'blog_pre': str(blog_list[pre_pos]),
                'blog_next': str(blog_list[next_pos]),
                'comments': comments,
                'comments_count': comments_count
            })
        else:
            return HttpResponseRedirect('/')


# 刷新验证码
class RefreshView(View):
    def get(self, request):
        to_json_response = dict()
        to_json_response['status'] = 1
        to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
        to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])
        return HttpResponse(json.dumps(to_json_response), content_type='application/json')


class AddCommentsView(View):
    def post(self, request):
        essay_id = request.POST.get('essay_id', None)
        if essay_id:
            comments = request.POST.get('comments', "")
            if comments:
                essay_comments = Comments()

                # get()只能取得一条数据，多条会报错
                # filter()可以返回一个数组
                essay = LofterModel.objects.get(id=int(essay_id))
                essay_comments.essay = essay
                essay_comments.comments = comments
                if not request.user.is_authenticated():
                    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                        user_ip = request.META['HTTP_X_FORWARDED_FOR']
                    else:
                        user_ip = request.META['REMOTE_ADDR']
                    user_ip_star = generate_new_ip(user_ip)
                    essay_comments.anonymous_user = get_ip_pos(user_ip) + '[' + user_ip_star + ']'
                else:
                    essay_comments.comment_user = request.user
                essay_comments.save()
                return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type='application/json')


class UserIndexView(View):
    def get(self, request, uid):
        uid = int(uid)

        search_keywords = request.GET.get('keywords', '')

        if search_keywords:
            all_items = LofterModel.objects.filter(Q(author_id=uid),
                                                   Q(title__icontains=search_keywords) | Q(
                                                       content__icontains=search_keywords))
        else:
            all_items = LofterModel.objects.filter(author_id=uid)

        paginator = Paginator(all_items, 3)  # Show 8 contacts per page
        page = request.GET.get('page', '1')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)

        return render(request, 'user_index.html', {
            'contacts': contacts,
        })


class UserBlogView(View):
    def get(self, request, uid, bid):
        uid = int(uid)
        blog_id = int(bid)
        blog_item = LofterModel.objects.filter(id=blog_id)
        blog_list = LofterModel.objects.filter(author_id=uid).defer('title', 'timestamp', 'content',
                                                                    'fav_click', 'image').values_list('id', flat=True)
        blog_list = list(blog_list)

        try:
            cur_pos = blog_list.index(blog_item[0].id)
        except:
            return render(request, 'active_fail.html', {'title': '404', 'msg': '访问页面不存在'})

        pre_pos = cur_pos - 1 if cur_pos != 0 else cur_pos
        next_pos = cur_pos + 1 if cur_pos != len(blog_list) - 1 else 0

        comments = Comments.objects.filter(essay=blog_id).order_by('-add_time')[:10]
        comments_count = Comments.objects.filter(essay=blog_id).count()
        if blog_item:
            return render(request, 'user_blog.html', {
                'uid': uid,
                'blog_item': blog_item[0],
                'blog_pre': str(blog_list[pre_pos]),
                'blog_next': str(blog_list[next_pos]),
                'comments': comments,
                'comments_count': comments_count
            })
        else:
            return HttpResponseRedirect('/')
