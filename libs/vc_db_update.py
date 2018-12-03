#!/usr/bin/env python3
# coding: utf-8
'''
- 收集 bilibili 上 vocaloid 相关的数据
- 对收集的数据进行合并去重并存入 sqlite 文件
- 根据需求下载相关视频与弹幕
'''

import time
import sqlite3
import requests

import json
import bs4
import re

# aid 编号 & 歌曲名称 & 上传时间
aids    = []
titles  = []
dates   = []

records = []

Debug = False
Detail = False
import sys

def _getMetaViaHtml(html):
    '''通过html页面获得相关信息'''
    soup = bs4.BeautifulSoup(html, "html.parser")

    # 获得搜索页面结果内容，若没有返回 False
    result = soup.findAll('div', class_='result-wrap clearfix')
    if len(result)<1:
        return(False)
    
    result = result[0]
    songs = result.findAll('li', class_='video')
    
    size = len(songs)
    print(size)

    if Debug:
        if size != 20:
            print(html)
            sys.exit(-1)

    for eachSong in songs:
        aid = eachSong.find('a', href=True)
        aid = re.match('.*av(\d+)', aid['href'])
        aid = aid.group(1)

        title = eachSong.find('a', class_='title').text

        date = eachSong.find('span', class_='so-icon time').text
        date = date.strip(' ').strip('\n').strip(' ')

        aids.append(aid)
        titles.append(title)
        dates.append(date)

    return(True)


def _get_data(url):
    '''收集指定页面的条目及相关信息'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    rs = requests.Session()

    # 获得 aid:编号 & title:歌曲名称 & date:上传时间，若不能获得则重试最多5次
    for i in range(5):
        r = rs.get(url, headers=headers)
        if r.status_code != 200:
            return -1

        html = r.text
        
        # 
        if _getMetaViaHtml(html):
            break
        else:
            print("Loop +1")
            time.sleep(1)
        
    # 相关统计数据
    watchs      = []    # 播放数
    dms         = []    # 弹幕数
    coins       = []    # 硬币数
    shares      = []    # 分享数
    replys      = []    # 评论数
    favorites   = []    # 收藏数

    aid_url = "http://api.bilibili.com/archive_stat/stat?aid=%s"

    for aid in aids:
        # 若html为空，则取内容，最多三次
        html = None
        for i in range(0, 3):
            try:
                html = rs.get(aid_url % aid, headers=headers).text
            except Exception as e:
                html = None
                
            if html is not None:
                break
        try:
            data = json.loads(html)
            watchs.append(data['data']['view'])
            dms.append(data['data']['danmaku'])
            coins.append(data['data']['coin'])
            shares.append(data['data']['share'])
            replys.append(data['data']['reply'])
            favorites.append(data['data']['favorite'])
        except TypeError:
            raise Exception("Error! %s, %s" % (aid_url % aid, html))

    # 汇总数据
    for i in range(0, len(titles)):
        # titles[i] is unicode
        records.append([('av%s' % aids[i]), dates[i], watchs[i], dms[i], coins[i],
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
    if Debug:
        end_page = 5
    
    '''下载VOCALOID中文曲按播放数排序的前50页页面'''
    # url = "http://search.bilibili.com/api/search?search_type=video&keyword=VOCALOID%E4%B8%AD%E6%96%87%E6%9B%B2&order=click&page="
    url = "http://search.bilibili.com/all?keyword=VOCALOID%E4%B8%AD%E6%96%87%E6%9B%B2&order=click&page="
    
    for i in range(start_page, end_page + 1):
        print("Page:%s" % i, end=', ')  
        # print(url+str(i)) # debug
        _get_data(url + str(i))

    _update_db(db_file)

    if Debug and Detail:
        for line in records:
            print(line)

    return 0


# Main
if __name__ == '__main__':
    '''main function'''
    update_data(end_page=2)

# End
