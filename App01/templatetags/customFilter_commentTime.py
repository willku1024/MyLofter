# _*_ coding: utf-8 _*_
__author__ = 'x_jwei@qq.com'
__date__ = '2017/10/15  14:38'

from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime
from django.utils import timezone


register = template.Library()


@register.filter(is_safe=True,needs_autoescape=True)
def commentTime(value, autoescape=True):
    dt = datetime.now()
    value = timezone.localtime(value)
    if dt.year-value.year == 0:
        if dt.month-value.month == 0:
            day = dt.day-value.day
            if day == 0:
                hour = dt.hour-value.hour
                if hour == 0:
                    mins = dt.minute-value.minute
                    if mins == 0:
                        return '刚刚'
                    else:
                        return str(mins) + '分钟前'
                return str(hour) + '小时前'
            elif day == 1:
                return '昨天 ' + value.strftime('%I:%M %p')
            elif day<= 5 and day >=2 :
                return str(day) + ' 天以前'

    return value
