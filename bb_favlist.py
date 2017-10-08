#!/usr/bin/env python3
# coding:utf-8
'''
用于下载指定用户在B站的收藏视频
'''
import argparse
import requests
import sys

if sys.version_info < (3, 0):
    raise SystemExit('Error: Need python3 envrionment')

# common uri
url_sidebar = 'http://space.bilibili.com/ajax/fav/getBoxList?mid=%s'
url_favorite = ('http://space.bilibili.com/ajax/fav/getList?'
                'mid=%s&pagesize=30&fid=%s&tid=0&pid=%s&order=fav_time')


def get_sidebar(mid):
    '''获得侧边栏中收藏夹列表'''
    url = url_sidebar % mid
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0)'
                       ' Gecko/20100101 Firefox/50.0')
    }
    rs = requests.Session()
    r = rs.get(url, headers=headers)
    if r.status_code != 200:
        return -1

    sidebar = []
    boxlist = r.json()
    for item in boxlist['data']['list']:
        sidebar.append({})
        sidebar[-1]['name'] = item['name']
        sidebar[-1]['count'] = item['count']
        sidebar[-1]['favid'] = item['fav_box']

    return sidebar


def get_favorite(mid, favid, page):
    '''获得指定收藏夹，指定页面的列表数据'''
    url = url_favorite % (mid, favid, page)
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0)'
                       ' Gecko/20100101 Firefox/50.0')
    }
    rs = requests.Session()
    r = rs.get(url, headers=headers)
    if r.status_code != 200:
        return -1
    boxlist = r.json()
    pages = boxlist['data']['pages']

    favlist = []
    for item in boxlist['data']['vlist']:
        favlist.append({})
        favlist[-1]['avnum'] = 'av' + str(item['aid'])
        favlist[-1]['uploadtime'] = item['pubdate']
        favlist[-1]['name'] = item['title']
        favlist[-1]['owner'] = item['owner']['name']
        favlist[-1]['playnum'] = item['play_num']
        favlist[-1]['dmnum'] = item['stat']['danmaku']

    return pages, favlist


def get_all_favlist(mid, favid):
    '''遍历指定收藏夹，获得所有列表数据'''
    pages, favlist = get_favorite(mid, favid, 1)

    if pages > 1:
        for i in range(2, pages + 1):
            p, list = get_favorite(mid, favid, i)
            favlist.extend(list)

    return favlist


def download(avnum, title):
    '''下载指定avnum视频'''
    import subprocess
    url = 'http://www.bilibili.com/video/' + avnum
    subprocess.call(
        'you-get -o ./video/favorite/%s "%s" > /dev/null 2>&1' % (title, url), shell=True)
    return 0


# Main
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mid', action='store', default='25527367',
                        help='mid of bilibili space')
    parser.add_argument('-t', '--title', action='store', default=u'VC之家', 
                        help='title name, default is "VC" ')
    parser.add_argument('-v', '--view', action='store_true',
                        help='view only, no download')
    args = parser.parse_args()

    mid = args.mid
    title = args.title
    s_list = get_sidebar(mid)
    for item in s_list:
        if item['name'] == title: # 获得指定名称文件夹列表
            list = get_all_favlist(mid, item['favid'])

    if args.view:
        print('### View Only ###')
        for item in list:
            print(item)
    else:
        print('### Download... ###')
        for item in list:
            print(item)
            download(item['avnum'], title)
