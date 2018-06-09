#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: GYK  Time:2018/4/6


import requests
import re
import json
from requests.exceptions import RequestException
from multiprocessing import Pool


#获取html 的文本 键  值
def getOnePage(url):
    try:
        headers = {
            'Host': 'maoyan.com',
            'User-Agent': 'User-Agent  Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN'
        }
        response = requests.get(url,headers=headers)

        if(response.status_code == 200):
            return response.text

        return None
    except RequestException:
        return None

#正则表达式获取需要的内容，并放入字典中
def parseOnePage(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d*)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">'
                         +'(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?).*?fraction">(.*?)</i></p>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3],
            'time':item[4],
            'score':item[5]+item[6]
        }

#写入文本文件
def writeToFile(content):
    with open("maoyan.txt",'a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + "\n")
        f.close()

#main函数
def main(offset):
    url = "http://maoyan.com/board/4?offset=" + str(offset)
    html = getOnePage(url)


    for item in parseOnePage(html):
        print(item)
        writeToFile(item)

#入口
if __name__ == '__main__':
    #main(0)
    # for i in range(10):
    #     print(i)
    #     main(i*10)
    #多线程抓取
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])
