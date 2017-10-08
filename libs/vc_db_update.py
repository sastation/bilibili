#!/usr/bin/env python3
# coding: utf-8
'''
- 收集 bilibili 上 vocaloid 相关的数据
- 对收集的数据进行合并去重并存入 sqlite 文件
- 根据需求下载相关视频与弹幕
'''

import time
import sqlite3
import bs4
import requests
import json

records = []


def _get_data(url):
    '''收集指定页面的条目及相关信息'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }

    rs = requests.Session()
    r = rs.get(url, headers=headers)
    if r.status_code != 200:
        return -1

    html = r.text
    soup = bs4.BeautifulSoup(html, "html.parser")

    # aid 编号
    aids = []
    for line in soup.find_all(class_="search-watch-later icon-later-off"):
        aids.append(line.attrs["data-aid"])

    # 歌曲名称
    titles = []
    for title in soup.find_all(class_="title"):
        try:
            titles.append(title.contents[0].strip())
        except AttributeError:
            titles.append("-")

    # 上传时间
    dates = []
    for date in soup.find_all(class_="so-icon time"):
        dates.append(date.contents[2].strip())

    # 相关统计数据
    watchs = []     # 播放数
    dms = []        # 弹幕数
    coins = []      # 硬币数
    shares = []     # 分享数
    replys = []    # 评论数
    favorites = []  # 收藏数

    aid_url = "http://api.bilibili.com/archive_stat/stat?aid=%s"
    for aid in aids:
        html = rs.get(aid_url % aid, headers=headers).text
        data = json.loads(html)
        watchs.append(data['data']['view'])
        dms.append(data['data']['danmaku'])
        coins.append(data['data']['coin'])
        shares.append(data['data']['share'])
        replys.append(data['data']['reply'])
        favorites.append(data['data']['favorite'])

    # 汇总数据
    for i in range(0, len(titles)):
        # titles[i] is unicode
        records.append(['av'+aids[i], dates[i], watchs[i], dms[i], coins[i],
                        shares[i], replys[i], favorites[i], titles[i]])

    rs.close()
    return 0


def _update_db(db_file):
    conn = sqlite3.connect(db_file)

    # 得到数据库中所有avnum列表
    avs = []
    curs = conn.execute('select avnum from bbvc;')
    lines = curs.fetchall()
    for item in lines:
        avs.append(item[0])

    # 更新数据库
    update_time = time.strftime('%Y-%m-%d', time.localtime())
    for line in records:
        # 若已有记录则更新：播放数、弹幕数、更新日期
        # 若没有记录则插入新记录
        if line[0] in avs:
            conn.execute('update bbvc set updatetime=?, playnum=?, dmnum=? '
                         ',v_coin=?, v_share=?, v_reply=?, v_favorite=?'
                         ' where avnum=?;',
                         (update_time, line[2], line[3], line[4], line[5],
                          line[6], line[7], line[0]))
        else:
            conn.execute('insert into bbvc'
                ' (avnum, uploadtime, playnum, dmnum, v_coin, v_share,'
                ' v_reply, v_favorite, title, updatetime)'
                ' values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
                (line[0], line[1], line[2], line[3], line[4], line[5],
                 line[6], line[7], line[8], update_time))
            avs.append(line[0])

    # 更新本次播放数过10万的 palacetime 字段
    conn.execute('update bbvc set palacetime=? '
                 ' where playnum>99999 and palacetime is null;',
                 (update_time,))
    conn.commit()
    conn.close()
    return 0


def update_data(db_file='vc_test.db', start_page=1, end_page=50):
    '''下载VOCALOID中文曲按播放数排序的前50页页面'''
    url = ("http://search.bilibili.com/all?keyword="
           "VOCALOID%E4%B8%AD%E6%96%87%E6%9B%B2&order=click"
           "&page=")
    for i in range(start_page, end_page + 1):
        _get_data(url + str(i))

    _update_db(db_file)

    return 0


# Main
if __name__ == '__main__':
    '''main function'''
    update_data(end_page=50)

# End
