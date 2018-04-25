# _*_ coding: utf-8 _*_
__author__ = 'x_jwei@qq.com'
__date__ = '2017/9/12  22:13'


from django import template

from django.utils.html import format_html

register = template.Library()  # 注册到django的语法库


@register.simple_tag
def guess_page(current_page, loop_num):
    offset = abs(current_page - loop_num)

    if offset < 2:

        if current_page == loop_num:

            page_ele = '''<a class="active item" href="?page=%s">%s</a>''' % (loop_num, loop_num)
        else:

            page_ele = '''<a class=" item" href="?page=%s">%s</a>''' % (loop_num, loop_num)

        return format_html(page_ele)

    else:

        return ''