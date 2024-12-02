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
        favlist[-1]['page'] = item['page']

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


def download(bvid, folder, page=1):
    '''下载指定avnum视频'''
    import subprocess
    url = 'https://www.bilibili.com/video/%s' % bvid
    
    # print('you-get -o %s "%s"' % (folder, url))
    cmd = 'you-get -o %s "%s"' %(folder, url)
    if page > 1: # multi-pv
        cmd = "%s --playlist" % cmd

    # 先偿试下载720p若失败以480p下载再失败以默认码率偿试下载，若3次都失败输出错误bvid
    #code = subprocess.call("%s -c cookie.txt --format=dash-flv720" % cmd, shell=True)
    # 视频格式有变化，dash-flv{720,480,360}-{AV1,AVC,HEVC}, 默认使用, 这里默认使用720-AVC
    code = subprocess.call("%s -c cookie.txt --format=dash-flv720-AVC" % cmd, shell=True)
    if code != 0:
        code = subprocess.call("%s --format=dash-flv480-AVC" % cmd, shell=True)
    if code != 0:
        code = subprocess.call(cmd, shell=True)
    if code != 0:
        print("Code: %s, bvid: %s" % (code, bvid))

    return 0


# Main
Folders = { 
        'VC.01': '55297967',
        'VC.02': '44835167',
        '歌舞': '54285067',
        '动画CG': '469182867',
        '临时': '498471367',
        'Ai': '1604743267',
        '极乐净土': '92676967',
        '经典歌曲': '1999390867'
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
        folder = "./video/%s" % args.folder # 下载目录
        for item in bvlist:
            #print(item)
            bvname = item['name']
            bvname = bvname.replace('"', "-") 
            bvname = bvname.replace("'", "-") 
            bvname = bvname.replace("/", "-") 
            bvname = bvname.replace("|", "-") 
            bvname = bvname.replace(":", "-") 
            bvname = bvname.replace("?", "-") 
            bvname = bvname.replace("*", "-") 
            fname = glob.escape(folder + "/" + bvname) # tranferred [] for glob.glob

            if len(glob.glob(fname+"*")) > 1: # 判断是否已下载
                print("%s is exist!" % fname)
                time.sleep(0.3)
            else:
                print("Warning: ", item['bvid'], item['name'], fname)
                if not '已失效视频' in item['name']:
                    download(item['bvid'], folder, item['page'])
    else:
        print('### View Only ###')
        for item in bvlist:
            print(item)
 
