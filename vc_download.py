#!/usr/bin/env python
# coding: utf-8
'''根据palace.list数据通过you-get下载相应的bilibili的视频'''
import subprocess


def main():
    '''main function'''

    avs = []
    # 载入已下载列表
    fs = open('download.list', 'r')
    for line in fs:
        avs.append(line.split(',')[0])
    fs.close()

    # 下载视频
    # fs = open('test.list', 'r')
    fs = open('palace.list', 'r')
    for line in fs:
        av = line.split(',')[1]

        # 跳过有下载记录的视频
        if av in avs:
            continue

        url = "http://www.bilibili.com/video/" + av
        cmd = subprocess.call('you-get -o video "%s" > /dev/null 2>&1' % url,
                              shell=True)
        if cmd:
            print "%s,wrong" % av
        else:
            print "%s,good" % av


# Main
if __name__ == '__main__':
    main()
# End
