#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: GYK  Time:2018/4/20

import pymongo
from requests.exceptions import RequestException
import requests
import json
from urllib.parse import urlencode

def get_index_page(start_page, id_page):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        'Referer': 'http://www.duitang.com/category/?cat=painting',
        'Accept': 'text/plain, */*; q=0.01',
        'Host': 'www.duitang.com',
        'Accept - Encoding': 'gzip,deflate, sdch',
        'Accept - Language': 'zh - CN, zh;q=0.8',
        'Connection': 'keep - alive',
    }
    data = {
        'include_fields': 'top_comments,'
                          'is_root, source_link, item, buyable, root_id, status, like_count, sender, album',
        'filter_id': '插画绘画',
        'start': start_page,
        '_': id_page,
    }
    url = 'http://www.duitang.com/napi/blog/list/by_filter_id/?' + urlencode(data)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错!')
        return None


def parse_page_index():
    i = 0
    n = 1498560199148
    while i < 23976:
        i = i + 24
        n = n + 1
        html = get_index_page(i, n)
        for n in range(24):

            data = json.loads(html.strip())  # 将json字典转换为python字典
            img_url = data['data']['object_list'][n]['photo']['path']   # 获取字典中的图片链接
            title = data['data']['object_list'][n]['msg']  # 获取字典中的标题
            post_sub.insert_one({'img_id': title, 'img_url': img_url})  # 插入到数据库中

            print(title, img_url)


if __name__ == '__main__':
    connection = pymongo.MongoClient()
    post_info = connection.duitang_painting
    post_sub = post_info.duitang
    parse_page_index()