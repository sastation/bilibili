#!/usr/bin/env python3
# coding: utf-8
'''
- 收集 bilibili 上 vocaloid 相关的数据
- 对收集的数据进行合并去重并存入 sqlite 文件
- 根据需求下载相关视频与弹幕
'''

import re
import json
import time
import sqlite3
import requests
#import bs4

# 所有记录
records = []

Debug = False
Detail = False


def _get_data(url):
    '''收集指定页面的条目及相关信息'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    rs = requests.Session()
    rs = requests.Session()
    r = rs.get(url, headers=headers)
    if r.status_code != 200:
        return -1

    html = r.text
    data = json.loads(html)["data"]

    ## aid 编号、bvid编号、歌曲名称、上传时间
    aids    = []
    bvids   = []
    titles  = []
    dates   = []

    for eachSong in data["result"]:
        aids.append(eachSong["aid"])
        bvids.append(eachSong["bvid"])

        uploadDate = time.strftime("%Y-%m-%d", time.localtime(eachSong["pubdate"]))
        dates.append(uploadDate)

        try:
            titles.append(eachSong["title"])
        except AttributeError:
            titles.append("-")

    # 单曲的统计数据
    watchs      = []    # 播放数
    dms         = []    # 弹幕数
    coins       = []    # 硬币数
    shares      = []    # 分享数
    replys      = []    # 评论数
    favorites   = []    # 收藏数

    detail_url = "https://api.bilibili.com/x/web-interface/view?bvid=%s"
    for bvid in bvids:
        # 若html为空，则取内容，最多三次
        html = None
        for i in range(0, 3):
            html = rs.get(detail_url % bvid, headers=headers).text
            if html is not None:
                break
        try:
            if Debug: print(html)

            data = json.loads(html)["data"]["stat"]
            watchs.append(data['view'])
            dms.append(data['danmaku'])
            coins.append(data['coin'])
            shares.append(data['share'])
            replys.append(data['reply'])
            favorites.append(data['favorite'])
        except TypeError:
            raise Exception("Error! %s, %s" % (detail_url % bvid, html))

    # 汇总数据
    for i in range(0, len(titles)):
        # titles[i] is unicode
        records.append([ bvids[i], dates[i], watchs[i], dms[i], coins[i], shares[i],
                        replys[i], favorites[i], titles[i], ('av%s' % aids[i]) ])

    rs.close()
    return 0

def _update_db(db_file):
    conn = sqlite3.connect(db_file)

    # 得到数据库中所有bvid列表
    bvids = []
    curs = conn.execute('select bvid from bbvc;')
    rows = curs.fetchall()
    for row in rows:
        bvids.append(row[0])

    # 更新数据库
    update_time = time.strftime('%Y-%m-%d', time.localtime())
    for line in records:
        # 若已有记录则更新：播放数、弹幕数、更新日期
        # 若没有记录则插入新记录
        if line[0] in bvids:
            conn.execute('update bbvc set updatetime=?, playnum=?, dmnum=? '
                         ',v_coin=?, v_share=?, v_reply=?, v_favorite=?'
                         ' where bvid=?;',
                         (update_time, line[2], line[3], line[4], line[5],
                          line[6], line[7], line[0]))
        else:
            conn.execute('insert into bbvc'
                ' (bvid, uploadtime, playnum, dmnum, v_coin, v_share,'
                ' v_reply, v_favorite, title, updatetime, avnum)'
                ' values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
                (line[0], line[1], line[2], line[3], line[4], line[5],
                 line[6], line[7], line[8], update_time, line[9]))
            bvids.append(line[0])

    # 更新本次播放数过10万的 palacetime 字段
    conn.execute('update bbvc set palacetime=? '
                 ' where playnum>99999 and palacetime is null;',
                 (update_time,))
    conn.commit()
    conn.close()
    return 0

def update_data(db_file='vc.db', start_page=1, end_page=50):
    if Debug: end_page = 5
    
    '''下载VOCALOID中文曲按播放数排序的前50页页面'''
    url = ("https://api.bilibili.com/x/web-interface/search/"
            "type?page=%s&order=click&search_type=video"
            "&keyword=VOCALOID中文曲")

    for i in range(start_page, end_page + 1):
        print("Page:%s" % i, end=', ')  # debug
        print(url) # debug

        _get_data(url % str(i))
        time.sleep(5) # 暂停5秒以避免被封

    _update_db(db_file)

    if Debug or Detail:
        for line in records:
            print(line)

    return 0


# Main
if __name__ == '__main__':
    '''main function'''
    update_data(db_file="vc.db", start_page=1, end_page=50)
    #update_data(end_page=2) # debug

# End
