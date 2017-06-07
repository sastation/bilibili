#!/usr/bin/env python
# coding: utf-8
'''
- 收集 bilibili 上 vocaloid 相关的数据
- 对收集的数据进行合并去重并存入 sqlite 文件
- 根据需求下载相关视频与弹幕
'''
import re
import time
import sqlite3
import bs4
import requests

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

    # 标题，AV号
    titles = []
    avs = []
    for title in soup.find_all(class_="title"):
        try:
            # titles.append(title.string.strip())
            titles.append(title.contents[0].strip())
        except AttributeError:
            titles.append("-")

        m = re.match(".*/(av\d+).*", title.attrs["href"])
        avs.append(m.group(1))

    # 播放数
    watchs = []
    for watch in soup.find_all(class_="so-icon watch-num"):
        play_num = watch.contents[2].strip()
        play_num = float(play_num.split(u'万')[0]) * 10000
        watchs.append(int(play_num))
        # print watch.stripped_strings.next()

    # 弹幕数
    bullets = []
    for bullet in soup.find_all(class_="so-icon hide"):
        bullets.append(int(bullet.contents[2].strip()))

    # 上传时间
    dates = []
    for date in soup.find_all(class_="so-icon time"):
        dates.append(date.contents[2].strip())

    for i in range(0, len(titles)):
        # titles[i] is unicode
        records.append([avs[i], dates[i], watchs[i], bullets[i], titles[i]])

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
            conn.execute('update bbvc set playnum=?, dmnum=?, updatetime=?'
                         ' where avnum=?;',
                         (line[2], line[3], update_time, line[0]))
        else:
            conn.execute('insert into bbvc'
                         ' (avnum, uploadtime, playnum, dmnum, '
                         ' title, updatetime)'
                         ' values(?, ?, ?, ?, ?, ?);',
                         (line[0], line[1], line[2], line[3],
                          line[4], update_time))
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
    for i in range(start_page, end_page+1):
        _get_data(url + str(i))
        if i % 10 == 0:
            time.sleep(5)

    _update_db(db_file)
    return 0


# Main
if __name__ == '__main__':
    '''main function'''
    update_data()

# End
