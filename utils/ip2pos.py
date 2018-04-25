# _*_ coding: utf-8 _*_
__author__ = 'x_jwei@qq.com'
__date__ = '2017/10/23  20:19'


import requests
import sys
from bs4 import BeautifulSoup


def get_ip_pos(ip):
    url = 'http://www.ip138.com/ips138.asp?ip={0}'.format(ip)
    r = requests.get(url)
    html = r.content
    soup = BeautifulSoup(html, 'lxml')
    position = soup.find('li')
    return position.string.split('：')[-1]


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    result = get_ip_pos("121.238.131.86")
    print result

