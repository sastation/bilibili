#!/usr/bin/env python3
# coding: utf-8
''' use ffmpeg to convert mp4|flv to mp3 '''

import os
import glob
import subprocess
import argparse


def convert_mp3(video_dir='./video'):
    lines = glob.glob("%s/*.flv" % video_dir)
    lines.extend(glob.glob("%s/*.mp4" % video_dir))

    for av_file in lines:
        # 获取路径与文件名
        path, fname = os.path.split(av_file)
        path = path.replace("video/", "audio/") # video目录改为audio
        mp3_file = "%s/%s.mp3" % (path, os.path.splitext(fname)[0]) # 文件为fname去除后缀加.mp3

        # 若 path 目录不存在则创建
        if not os.path.isdir(path):
            os.makedirs(path)
        
        # 若 mp3_file 已存在则跳过
        if os.path.isfile(mp3_file):
            print("%s is existed." % mp3_file)
            continue

        #print(mp3_file, os.path.exists(mp3_file))

        cmd = 'ffmpeg -n -i "%s" -f mp3 -vn -af "loudnorm=i=-14" "%s"' % (av_file.strip(), mp3_file)
        cmd = subprocess.call(cmd, shell=True)
        if cmd:
            status = "wrong"
        else:
            status = "good"
            
        print("convert %s to mp3 is %s" % (av_file.strip(), status))

    return 0


# Main
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', action='store', help='video path')

    args = parser.parse_args()
    if args.path:
        convert_mp3(args.path)
    else:
        parser.print_help()
# End
