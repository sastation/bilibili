#!/usr/bin/env python
# coding: utf-8
'''
- 对从bilibili上收集的vocaloid相关的数据进行处理
- 条件：
    1. 数据文件从最旧一次开始向前处理
    2. 挑出播放数超10万的记录，只记录最早一次
- 输出：以打印方式输出
'''

import re
import os
import glob

avs = []
lines = []


def match(file):
    '''对数据进行处理'''

    # 得到日期
    m = re.match(".*-(\d+)", file)
    if m:
        dtm = m.group(1)

    fs = open(file, 'r')
    for line in fs:
        # 跳过播放数未到10万的记录
        play_num = line.split(',')[2].split('万')[0]
        if float(play_num) < 10:
            continue

        # 跳过重复数据
        av = line.split(',')[0]
        if av in avs:
            continue
        avs.append(av)

        line = line.strip().split(",")
        line = "%s,%s,%s,%s" % (dtm, line[0], line[1], line[4])
        lines.append(line)
    fs.close()


def main():
    '''main function'''
    files = filter(os.path.isfile, glob.glob("vc.list-*"))
    files.sort(key=lambda x: os.path.getmtime(x))

    for file in files:
        # print "# %s" % file
        match(file)


# Main
if __name__ == '__main__':
    main()
    for line in lines:
        print line
# End
