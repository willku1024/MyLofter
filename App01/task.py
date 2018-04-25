# _*_ coding: utf-8 _*_
__file__ = 'task.py'
__author__ = 'x_jwei@qq.com'
__date__ = '2018/4/23  20:42'


from celery import task, platforms
from django.core.cache import cache
from App01.models import LofterModel

platforms.C_FORCE_ROOT = True

@task
def sync_database():
    for session_key in cache.iter_keys("fav_item_id_*"):
        item_id = session_key.split('_')[-1]
        exist_records = LofterModel.objects.filter(id=int(item_id))[0]
        exist_records.fav_click = int(cache.get(session_key))
        exist_records.save()


if __name__ == "__main__":
    pass