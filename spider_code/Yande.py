
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: GYK  Time:2018/4/15
from lxml import etree
import requests
import re
import time
import random
from bs4 import BeautifulSoup
import pymongo


def get_max_page(url, headers):
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    time.sleep(2)
    for h in soup.select('#post-list-posts > li > div.inner > a.thumb '):
        image_id = h.get('href').split('/')[-1]
        # post_sub.insert_one({'img_id': image_id})
        each_pic_id = 'https://yande.re' + h.get('href')
        print(image_id)
        get_img_url(each_pic_id, headers, image_id)


def get_img_url(id_url, headers, image_id):
    html = requests.get(id_url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    time.sleep(2)
    for i in soup.select('#image'):
        img_url = i.get('src')
        post_sub.insert_one({'img_id': image_id, 'img_url': img_url})  # insert_one:插入一条数据，for：遍历，  一条一条插入
        print(img_url)


if __name__ == '__main__':
    tag = input('请输入你要下载的类型（标签）:')
    max_page = input('请输入你要下载的页数：')
    for n in range(1, int(max_page) + 1):
        url = 'https://yande.re/post?page=' + str(n) + '&tags=' + str(tag)
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
        ]
        UA = random.choice(user_agent_list)
        headers = {'User-Agent': UA,
                   # 'Referer':'https://yande.re/post',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Host': 'yande.re',
                   'Accept - Encoding': 'gzip,deflate,br',
                   'Accept - Language': 'zh - CN, zh;q=0.8',
                   'Connection': 'keep - alive',
                   }
        connection = pymongo.MongoClient()  # 连接MongDB数据库
        post_info = connection.yande_test  # 指定数据库名称（yande_test），没有则创建
        post_sub = post_info.test  # 获取集合名：test
        get_max_page(url, headers)