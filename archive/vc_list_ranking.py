#!/usr/bin/env python
# coding: utf-8
'''
- 对从bilibili上收集的vocaloid相关的数据进行整理合并
- 条件：
    #0. 播放数超过10万
    1. 重复数据只取最新一条记录
    2. 数据文件从最近一次开始向前处理
- 输出：以打印方式输出
'''

import os
import glob

avs = []
lines = []


def match(file):
    '''对数据进行处理'''
    fs = open(file, 'r')
    for line in fs:
        # 跳过重复数据
        av = line.split(',')[0]
        if av in avs:
            continue
        avs.append(av)

        '''
        # 跳过播放数未到10万的记录
        play_num = line.split(',')[2].split('万')[0]
        if float(play_num) < 10:
            continue
        '''

        lines.append(line.strip())
    fs.close()


def main():
    '''main function'''
    files = filter(os.path.isfile, glob.glob("vc.list-*"))
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    for file in files:
        # print "# %s" % file
        match(file)


# Main
if __name__ == '__main__':
    main()
    for line in lines:
        print line
# End
