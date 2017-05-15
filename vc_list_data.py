#!/usr/bin/env python
# coding: utf-8
'''收集 bilibili 上 vocaloid 相关的数据'''

import re
import time
import bs4
import requests


def vocaloid(rs, url):
    '''收集指定页面的条目及相关信息'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    r = rs.get(url, headers=headers)
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
        watchs.append(watch.contents[2].strip())
        # print watch.stripped_strings.next()

    # 弹幕数
    bullets = []
    for bullet in soup.find_all(class_="so-icon hide"):
        bullets.append(bullet.contents[2].strip())

    # 上传时间
    dates = []
    for date in soup.find_all(class_="so-icon time"):
        dates.append(date.contents[2].strip())

    for i in range(0, len(titles)):
        str_out = (u"%s,%s,%s,%s,%s") % \
            (avs[i], dates[i], watchs[i], bullets[i], titles[i])
        print str_out.encode("utf-8")


def main():
    '''main function'''
    rs = requests.Session()
    url = ("http://search.bilibili.com/all?keyword="
           "VOCALOID%E4%B8%AD%E6%96%87%E6%9B%B2&order=click"
           "&page=")
    for i in range(1, 51):
        # print "# %s" % (url + str(i))
        vocaloid(rs, url+str(i))
        if i % 10 == 0:
            time.sleep(5)
    return 0


# Main
if __name__ == '__main__':
    main()
# End
