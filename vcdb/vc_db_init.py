#!/usr/bin/env python
# coding: utf-8
'''
- 收集 bilibili 上 vocaloid 相关的数据
- 对收集的数据进行合并去重并存入 sqlite 文件
- 根据需求下载相关视频与弹幕
'''
import sqlite3

DB_FILE = 'vc_test.db'
records = []


def create_table(db_file=DB_FILE):
    '''create table if db not exist'''
    conn = sqlite3.connect(db_file)
    conn.execute('create table IF NOT EXISTS bbvc '
                 ' (avnum vchar(25) primary key,'
                 'playnum integer, dmnum integer, title vchar(255),'
                 'uploadtime vchar(10), palacetime vchar(10),'
                 'updatetime vchar(10),downtime vchar(10),'
                 'downstatus vchar(5));'
                 )
    conn.close()


def import_data(db_file=DB_FILE):
    '''将数据从原来文本文件中导入'''
    conn = sqlite3.connect(db_file)
    # 读入排序数据
    fs = open('data/ranking.list', 'r')
    i = 0
    for line in fs:
        cols = line.strip().split(',')
        play_num = float(cols[2].split('万')[0]) * 10000
        cols[2] = int(play_num)
        cols[3] = int(cols[3])
        # title of cols[4] is str type (ascii?)
        conn.execute('insert into bbvc'
                     ' (avnum,uploadtime,playnum,dmnum,title)'
                     ' values(?,?,?,?,?);',
                     (cols[0], cols[1], cols[2], cols[3],
                      cols[4].decode('utf-8')))
        i = i + 1
        if i % 10 == 0:
            conn.commit()
    fs.close()

    # 读入殿堂数据
    fs = open('data/palace.list', 'r')
    for line in fs:
        cols = line.strip().split(',')
        cols[0] = '20%s-%s-%s' % (cols[0][0:2], cols[0][2:4], cols[0][4:6])
        # print cols[0], cols[1]
        conn.execute('update bbvc set palacetime=? where avnum=?',
                     (cols[0], cols[1]))
    conn.commit()
    fs.close()

    # 读入下载数据
    fs = open('data/download.list', 'r')
    for line in fs:
        cols = line.strip().split(',')
        # print cols[0], cols[1]
        conn.execute('update bbvc set downtime=?, downstatus=? where avnum=?',
                     ('2017-05-09', cols[1], cols[0]))
    conn.commit()
    conn.close()
    fs.close()

    return 0


def main():
    '''main function'''
    create_table()
    import_data()
    # return 0

    return 0


# Main
if __name__ == '__main__':
    main()
# End
