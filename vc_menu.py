#!/usr/bin/env python
# coding: utf-8
'''根据下载视频的XML字幕文件生成ass字幕文件'''
import subprocess
import glob
import os


def convert_menu(video_dir="./video"):
    '''下载视频'''
    lines = glob.glob('%s/*.cmt.xml' % video_dir)

    for line in lines:
        file = line.strip()

        # 转换字幕
        if not os.path.isfile('%s.ass' % file):
            cmd = './video/danmaku2ass/danmaku2ass.py -o "%s.ass" -s 1920x1080 -fn "微软雅黑" -fs 52 -a 0.8 -dm 12 -ds 6 "%s"' % (
                file, file)
            cmd = subprocess.call(cmd, shell=True)
            if cmd:
                status = 'wrong'
            else:
                status = 'good'
        else:
            status = 'exist'

        print 'convert %s is %s' % (file, status)

    return 0


# Main
if __name__ == '__main__':
    convert_menu()
# End
