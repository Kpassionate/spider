# MeiZi_wang
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: GYK  Time:2018/4/6
import urllib.request
import urllib
import re
from collections import deque
import requests as rs

def get_data(url):  # 获取页面源码
    try:
        data = urllib.request.urlopen(url).read().decode("utf-8")
        return data  # 没有异常返回字符串
    except:
        return ""  # 发生异常返回空


def get_all_http(data):  # 获取所有的http链接
    try:
        my_list = http_regex.findall(data)
        return my_list
    except:
        return []


def download(url):  # 下载图片
    hd = {}
    hd['referer'] = url  # 用于突破防盗链下载    referer + 当前网址
    t = rs.get(url, headers=hd).content
    name = url.split('/')
    # 切片获取图片name
    name = "{}.{}.{}.{}".format(name[-3], name[-2], name[-1][0:2], name[-1][2:])
    file(url, t, name)


def file(url, t, name):
    with open('E:\\123\\' + name, 'wb')as f:  # 写入指定文件夹
        f.write(t)
        print('已下载：', url)

def bfs(url_str):
    url_queue = deque([])  # url队列
    pic_queue = deque([])  # pic 队列
    url_queue.append(url_str)  # 添加一级域名
    while len(url_queue) != 0:  # 当队列不为空
        url = url_queue.popleft()  # 弹出一个网址
        data = get_data(url)  # 获取网页源码
        url_list = get_all_http(data)  # 获取源码中的所有链接到url_list
        for i in url_list:  # 遍历所有链接
            if pic_regex.findall(i):  # 如果正则匹配到大图片网址
                download(i)  # 直接下载
            elif regex.findall(i):  # 如果匹配到大图的上一级网址
                if i not in pic_queue:  # 如果该链接不在队列中
                    pic_queue.append(i) # 添加到图片队列
            elif i.find("mzitu") or i.find("meizitu"):  # 判断是否是该网站域名
                if i not in url_queue:  # 判断是否在 url队列
                    url_queue.append(i) # 添加到url队列

        while len(pic_queue) !=0:  # 图片队列不为0
            url_pic = pic_queue.popleft()  # 弹出一个链接
            data1 = get_data(url_pic)  # 过去该链接的源码
            pic_list = get_all_http(data1)  # 返回 源码中的所有链接
            for j in pic_list:  # 遍历所有链接
                # print(j)  # 打印
                if pic_regex.findall(j):  # 如果匹配图片链接成功
                    print("开始下载",j)
                    download(j)  # 开始下载
                    print("下载完成", j)
                elif regex.findall(j):  # 如果匹配图片上一级链接成功
                    if j not in pic_queue:  # 不在pic队列时
                        pic_queue.append(j)  # 添加到pic队列
                elif j.find("mzitu") or j.find("meizitu"):  # 如果是网站下属域名
                    if j not in url_queue:  # 判断是否存在url队列
                        url_queue.append(j)  # 不存在则添加



http_regex = re.compile(r"(http://\S*?)[\"|>|)]", re.IGNORECASE)  # http预编译
regex = re.compile("(http://[www|m].mzitu.com/\\d+?)")  # 图片id网址预编译
pic_regex = re.compile("http://i\.meizitu\.net/201[7|8]/\\d{2}/.*?\.jpg")  # 图片链接预编译
bfs("http://www.mzitu.com/")


