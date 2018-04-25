# _*_ coding: utf-8 _*_
__author__ = 'x_jwei@qq.com'
__date__ = '2017/9/28  18:30'


import requests
import re
import sys
from bs4 import BeautifulSoup

def get_song_list(list_id):
    headers = {'Referer': 'http://music.163.com/',
               'Host': 'music.163.com',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
               }

    play_url = 'http://music.163.com/playlist?id={0}'.format(list_id)
    s = requests.session()
    s = BeautifulSoup(s.get(play_url, headers=headers).content,'lxml')
    main = s.find('ul', {'class': 'f-hide'})

    music_list = {}
    offset = 0
    singer = ''
    for music in main.find_all('a'):
        # singer = get_song_singer('http://music.163.com'+ music['href'])
        music_list[offset] = [str(music['href']), str(music.text), singer]
        offset += 1
    music_list["count"] = offset

    return music_list


def get_song_singer(song_url):
    r = requests.get(song_url)
    html = r.content
    # soup = BeautifulSoup(html,'lxml')
    pattern = re.compile('<title>.*</title>')
    title= pattern.findall(html)
    return '&nbsp;---&nbsp;'+title[0].split('-')[1]


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    music_list = get_song_list("512409331")
    music_songer = get_song_singer("http://music.163.com/song?id=65592")
    print music_list
    print music_songer
