#!/usr/bin/env python3
# coding:utf-8
'''根据avid下载所有历史弹幕'''

import sys
import requests
avid = 21044350

# 历史弹幕列表
url = "https://comment.bilibili.com/rolldate,%s" % avid
req = requests.Session()
rs = req.get(url)
if rs.status_code != 200:
    # return(0)
    sys.exit(0)
html = rs.text
items = eval(html)

# 获得所有历史弹幕
rows = []
for item in items:
    # url = "https://comment.bilibili.com/dmroll,1501689600,21044350"
    url = "https://comment.bilibili.com/dmroll,%s,%s" % (item['timestamp'], avid)
    req = requests.Session()
    rs = req.get(url)

    if rs.status_code != 200:
        # return -1
        print("wrong")
    
    xml = rs.text
    for line in xml:
        if re.match("<d ", line):
            rows.append(line)

#! # 去重: 方法一, 保持原有顺序
#! from collections import OrderedDict
#! xmls = list(OrderedDict.fromkeys(rows))

# 去重：方法二, 不能保证原有顺序
xmls = list(set(rows))

# 添加第一行
xmls.insert(0, "<?xml version=\"1.0\" encoding=\"UTF-8\"?><i>"
            "<chatserver>chat.bilibili.com</chatserver>"
            "<chatid>%s</chatid><mission>0</mission>"
            "<maxlimit>1200000</maxlimit>"
            "<max_count>1200000</max_count>" % avid)

# 添加最后一行
xmls.append("</i>")

# 保存弹幕
fs = open("%s.xml" % (avid, item['timestamp']), 'w', encoding='utf-8')
print(xmls, file=fs)
fs.close()
