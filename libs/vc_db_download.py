#!/usr/bin/env python3
# coding: utf-8
'''根据DB中palacetime数据通过you-get下载相应的bilibili的视频'''
import subprocess
import time
import sqlite3


def download(dbfile='vc_test.db'):
    '''下载视频'''
    conn = sqlite3.connect(dbfile)

    # 得到数据库中未下载的殿堂avnum列表
    avs = []
    curs = conn.execute('select * from bbvc'
                        ' where (downstatus!="good" or downstatus isnull)'
                        ' and palacetime notnull;')
    lines = curs.fetchall()
    for item in lines:
        avs.append(item[0])

    # 下载视频
    download_time = time.strftime('%Y-%m-%d', time.localtime())
    for av in avs:
        url = "http://www.bilibili.com/video/" + av
        print('you-get -o video "%s" > /dev/null 2>&1' % url)

        #!cmd = subprocess.call('you-get -o video "%s" > /dev/null 2>&1' % url,
        #!                      shell=True)

        cmd = subprocess.call('you-get -o video "%s" ' % url, shell=True)
        if cmd:
            status = 'wrong'
        else:
            status = 'good'
        conn.execute('update bbvc set downtime=?, downstatus=?'
                     ' where avnum=?;',
                     (download_time, status, av))

    conn.commit()
    conn.close()
    return 0


# Main
if __name__ == '__main__':
    download()
# End
