# _*_ coding: utf-8 _*_
__author__ = 'x_jwei@qq.com'
__date__ = '2017/10/5  13:50'

import hashlib
import random
import time


def generate_random_str(randomlength=10):
    def md5_code():
        timestamp = str(int(time.time()))
        m = hashlib.md5()
        m.update(timestamp)
        return m.hexdigest()

    hash_code = []
    hash_code += [ random.choice(md5_code()) for i in range(0,randomlength) ]
    return ('').join(hash_code).upper()

if __name__ == "__main__":
    print generate_random_str()
