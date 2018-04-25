# _*_ coding: utf-8 _*_
__author__ = 'x_jwei@qq.com'
__date__ = '2017/9/24  21:10'

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True,needs_autoescape=True)
@stringfilter
def shorten_content(value, arg, autoescape=True):
    length = len(value)
    arg = int(arg)
    if length >= arg:
        new = value[:arg] + " ..."
    else:
        new = value +'<br/>'*3
        new = mark_safe(new)
    return new

# register.filter('shorten_content', shorten_content)