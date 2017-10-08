#!/usr/bin/env python3
# coding: utf-8
'''根据下载视频的XML字幕文件生成ass字幕文件'''
import os
import sys
import glob
import subprocess
import argparse

if sys.version_info < (3, 0):
    raise SystemExit('Error: Need python3 envrionment')


def convert_menu(video_dir='./video', exe_dir=None):
    '''指定目录中的下载视频字幕由xml转换成ass'''
    lines = glob.glob('%s/*.cmt.xml' % video_dir)

    for line in lines:
        file = line.strip()

        # 转换字幕
        if not os.path.isfile('%s.ass' % file):
            cmd = (exe_dir + '/danmaku2ass.py -o "%s.ass" -s 1920x1080'
                   ' -fn "微软雅黑" -fs 52 -a 0.8 -dm 12 -ds 6 "%s"'
                   % (file, file)
                   )
            cmd = subprocess.call(cmd, shell=True)
            if cmd:
                status = 'wrong'
            else:
                status = 'good'
        else:
            status = 'exist'

        print('convert %s is %s' % (file + '.ass', status))

    return 0


# Main
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', action='store', help='video path')
    parser.add_argument('-e', '--exe', action='store',
                        help='danmaku2ass.py path',
                        default='./video/danmaku2ass/')
    args = parser.parse_args()
    if args.path:
        convert_menu(args.path, args.exe)
    else:
        parser.print_help()
# End
