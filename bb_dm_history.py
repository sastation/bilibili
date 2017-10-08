#!/usr/bin/env python3
# coding:utf-8
'''根据avid下载所有历史弹幕'''

import requests
avid = 21044350

# 历史弹幕列表
url = "https://comment.bilibili.com/rolldate,%s" % avid
req = requests.Session()
rs = req.get(url)
if rs.status_code != 200:
    return -1
html = rs.text
items = eval(html)

# 指定某天的历史弹幕内容
for item in items:
    # url = "https://comment.bilibili.com/dmroll,1501689600,21044350"
    url = "https://comment.bilibili.com/dmroll,%s,%s" % (item['timestamp'], avid)
    req = requests.Session()
    rs = req.get(url)

    if rs.status_code != 200:
        # return -1
        print("wrong")
    xml = rs.text
    print(len(xml))


