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
        # 获取文件名，含路径不含扩展名
        # new_file = os.path.splitext(os.path.split(av_file)[1])[0]
        mp3_file = os.path.splitext(av_file)[0] + ".mp3"
        cmd = 'ffmpeg -n -i "%s" -f mp3 -vn "%s"' % (av_file.strip(), mp3_file)

        if not os.path.isfile(mp3_file):
            cmd = subprocess.call(cmd, shell=True)
            if cmd:
                status = "wrong"
            else:
                status = "good"
        else:
            status = 'exist'
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
