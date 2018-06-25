#!/usr/bin/env python3
# coding:utf-8
'''根据avid下载所有历史弹幕'''

import os
import requests


def history_dm(avid, folder):
    # 历史弹幕列表
    url = "https://comment.bilibili.com/rolldate,%s" % avid
    req = requests.Session()
    rs = req.get(url)
    if rs.status_code != 200:
        return(0)

    html = rs.text
    items = eval(html)

    # 获得所有历史弹幕
    rows = []
    for item in items:
        url = "https://comment.bilibili.com/dmroll,%s,%s" % (item['timestamp'], avid)
        req = requests.Session()
        rs = req.get(url)

        if rs.status_code != 200:
            # return -1
            print("wrong")

        xml = rs.text
        fs = open("%s/%s_.xml" % (folder, item['timestamp']), 'w', encoding="utf-8")
        print(xml, file=fs)
        fs.close()


def merge_dm(avid, folder, limitation=10000):
    import glob
    import re

    # 获得指定目录中所有历史弹幕文件名并排序
    items = glob.glob("%s/*_.xml" % folder)
    items.sort()

    for i in range(0, len(items), limitation):
        files = items[i:i+limitation]
        # 获得文件中所有内容
        rows = []
        for item in files:
            fs = open(item, "r", encoding="utf-8")
            lines = fs.readlines()
            fs.close()

            for line in lines:
                if re.match("<d ", line):
                    rows.append(line)

        # 去重: 方法一, 保持原有顺序
        from collections import OrderedDict
        xmls = list(OrderedDict.fromkeys(rows))

        # # 去重：方法二, 不能保证原有顺序
        # xmls = list(set(rows))

        # 添加第一行
        xmls.insert(0, "<?xml version=\"1.0\" encoding=\"UTF-8\"?><i>"
                    "<chatserver>chat.bilibili.com</chatserver>"
                    "<chatid>%s</chatid><mission>0</mission>"
                    "<maxlimit>1200000</maxlimit>"
                    "<max_count>1200000</max_count>\n" % avid)

        # 添加最后一行
        xmls.append("</i>\n")

        # 保存弹幕, 文件名：%folder/%avid_%i.xml
        fs = open("%s/%s_%s.cmt.xml" % (folder, avid, i), 'w', encoding='utf-8')
        print(''.join(xmls), file=fs)
        fs.close()


if __name__ == '__main__':
    avid = 21044350
    folder = "test%s" % avid
    if not os.path.isdir(folder):
        os.mkdir(folder)

    # history_dm(avid, folder)
    merge_dm(avid, folder, 7)

