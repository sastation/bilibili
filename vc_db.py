#!/usr/bin/env python3
# coding: utf-8
'''
- 收集 bilibili 上 vocaloid 相关的数据
- 对收集的数据进行合并去重并存入 sqlite 文件
- 根据需求下载相关视频与弹幕
'''
import argparse

from libs import vc_update as dbupdate
from libs import vc_download as dbdownload
db_file = 'vc.db'


# Main function
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--update', action='store_true',
                        help='update db data')
    parser.add_argument('-d', '--download', action='store_true',
                        help='download video')
    args = parser.parse_args()

    if args.update:
        print('update db data')
        dbupdate.update_data(db_file, 1, 50)
    elif args.download:
        print('download video')
        dbdownload.download(db_file)
    else:
        parser.print_help()
# End
