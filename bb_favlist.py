#!/usr/bin/env python3
# coding:utf-8
'''
用于下载指定用户在B站的收藏视频
'''
import argparse
import requests
import sys
import glob

if sys.version_info < (3, 0):
    raise SystemExit('Error: Need python3!')

def get_favorite(mid, page):
    '''获得指定收藏夹，指定页面的列表数据'''
    
    # API URL for contents of favorite folder 
    # full url: https://api.bilibili.com/x/v3/fav/resource/list?media_id=44835167&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&jsonp=jsonp
    url_favorite = 'https://api.bilibili.com/x/v3/fav/resource/list?media_id=%s&pn=%s&ps=20'
    
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0)'
                       ' Gecko/20100101 Firefox/50.0')
    }

    url = url_favorite % (mid, page)
    rs = requests.Session()
    r = rs.get(url, headers=headers)
    if r.status_code != 200:
        return -1

    bvlist = r.json()['data']['medias']
    if bvlist is None:
        return None

    favlist = []
    for item in bvlist:
        favlist.append({})
        favlist[-1]['bvid'] = item['bvid']
        favlist[-1]['uploadtime'] = item['pubtime']
        favlist[-1]['name'] = item['title']
        favlist[-1]['owner'] = item['upper']['name']
        favlist[-1]['playnum'] = item['cnt_info']['play']
        favlist[-1]['dmnum'] = item['cnt_info']['danmaku']

    return favlist


def get_all_favlist(mid):
    '''遍历指定收藏夹，获得所有列表数据'''
    favlist = []

    for i in range(1, 50): # 收藏夹最多999个视频，一页20个，最多50页
        bvlist = get_favorite(mid, i)
        if bvlist is None:
            break
        favlist.extend(bvlist)

    return favlist


def download(bvid, folder):
    '''下载指定avnum视频'''
    import subprocess
    url = 'https://www.bilibili.com/video/%s' % bvid
    
    # print('you-get -o %s "%s"' % (folder, url))
    subprocess.call('you-get -o %s "%s"' % (folder, url), shell=True)
    return 0


# Main
Folders = { 
        'VC.01': '55297967',
        'VC.02': '44835167',
        '歌舞': '54285067',
        '动画CG': '469182867',
        '极乐净土': '92676967',
        '临时': '498471367'
    }

if __name__ == '__main__':
    import time
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='folder', action='store',  help='folder name')
    parser.add_argument('-l', dest='list', action='store_true', help='list folders')
    parser.add_argument('-d', dest='download', action='store_true', help='download mode, default is view mode')
    args = parser.parse_args()

    if args.list:
        for item in Folders:
            print(item, Folders[item])
        sys.exit(0)

    if args.folder is None: # 没有文件夹名则打印帮助
        parser.print_help(sys.stderr)
        sys.exit(-1)

    # 获取名称对应的mid号
    mid = Folders[args.folder]

    bvlist = get_all_favlist(mid)

    if args.download:
        print('### Download... ###')
        folder = "./video/favorite/%s" % args.folder # 下载目录
        for item in bvlist:
            print(item)
            bvname = item['name']
            file = folder + "/" + bvname + "*"
            if len(glob.glob(file)) > 1: # 判断是否已下载
                print("%s is exist!" % file)
                time.sleep(1)
            else:
                download(item['bvid'], folder)
    else:
        print('### View Only ###')
        for item in bvlist:
            print(item)
 
