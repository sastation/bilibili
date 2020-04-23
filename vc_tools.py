#!/usr/bin/env python3
# coding: utf-8
'''
用于对vc数据库进行查询的一组工具
'''

import sqlite3
import argparse

# 数据库文件
db_file = 'vc.db'

class queryDB(object):
    '''查询DB工具类'''
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.columns = ('bvid, uploadtime, updatetime, palacetime, downstatus,'
                        ' playnum, dmnum, v_coin, v_reply, v_favorite, v_share, title')

    def __del__(self):
        self.conn.close()

    def _output(self, lines, title=None):
        '''将数据格式化输出'''
        if title is None:
            print(self.columns)
        else:
            print(title)

        for row in lines:
            for item in row:
                if item is None:
                    print('-', end=" ")
                else:
                    print(item, end=" ")
            print('')

    def _query(self, sql, title=None):
        '''执行SQL语句，将结果返回'''
        curs = self.conn.execute(sql)
        rows = curs.fetchall()
        self._output(rows, title)
        return rows

    def all(self):
        '''输出所有记录'''
        sql = ('select %s from bbvc;' % self.columns)
        return self._query(sql)

    def avid(self, avnum='%'):
        '''按 编号/id 进行模糊查找'''
        sql = ('select %s from bbvc where avnum like "%s";'
               % (self.columns, avnum))
        return self._query(sql)

    def name(self, title='%'):
        '''按标题进行模糊查找'''
        sql = ('select %s from bbvc where title like "%s";'
               % (self.columns, title))
        return self._query(sql)

    def upload(self, day=None):
        '''按上传时间进行模糊查找'''
        if day is None:
            sql = ('select uploadtime, count(*) from bbvc group by uploadtime'
                   ' order by uploadtime desc;')
            return self._query(sql, 'uplaodtime, count')
        else:
            sql = ('select %s from bbvc where uploadtime like "%s";'
                   % (self.columns, day))
            return self._query(sql)

    def palace(self, day=None):
        '''按殿堂时间进行模糊查找'''
        if day is None:
            sql = ('select palacetime, count(*) from bbvc group by palacetime'
                   ' order by palacetime desc;')
            return self._query(sql, 'palace-time, count')
        else:
            sql = ('select %s from bbvc where palacetime like "%s"'
                   ' order by palacetime;' % (self.columns, day))
            return self._query(sql)

    def download(self, day=None):
        '''按下载时间进行查询'''
        if day is None:
            sql = ('select downtime, count(*) from bbvc group by downtime'
                   ' order by downtime desc;')
            return self._query(sql, 'download-time, count')
        else:
            sql = ('select %s from bbvc where downtime like "%s"'
                   ' order by downtime;' % (self.columns, day))
            return self._query(sql)

    def update(self, day=None):
        '''按更新时间进行查询'''
        if day is None:
            sql = ('select updatetime, count(*) from bbvc group by updatetime'
                   ' order by updatetime desc;')
            return self._query(sql, 'update-time, count')
        else:
            sql = ('select %s from bbvc where updatetime like "%s";'
                   % (self.columns, day))
            return self._query(sql)

    def statistics(self, lastnum=7):
        '''overview report and last <lastnum> records'''
        sql = 'select count(*) from bbvc;'
        self._query(sql, 'Total')
        print('-' * 79)

        sql = 'select count(*) from bbvc where updatetime isnull;'
        self._query(sql, 'none-updatime-count')
        sql = ('select count(*) from bbvc where updatetime notnull;')
        self._query(sql, 'update-count')
        sql = ('select updatetime, count(*) from bbvc'
               ' where updatetime notnull group by updatetime'
               ' order by updatetime desc limit %i;' % lastnum)
        self._query(sql, 'update-time, count # last %i records' % lastnum)
        print('-' * 79)

        sql = 'select count(*) from bbvc where palacetime isnull;'
        self._query(sql, 'none-palace-count')
        sql = ('select count(*) from bbvc where palacetime notnull;')
        self._query(sql, 'palace-count')
        sql = ('select palacetime, count(*) from bbvc'
               ' where palacetime notnull group by palacetime'
               ' order by palacetime desc limit %i;' % lastnum)
        self._query(sql, 'palace-time, count # last %i records' % lastnum)
        print('-' * 79)

        sql = 'select count(*) from bbvc where downtime isnull;'
        self._query(sql, 'none-download-count')
        sql = ('select count(*) from bbvc where downtime notnull;')
        self._query(sql, 'download-count')
        sql = ('select downtime, count(*) from bbvc'
               ' where downtime notnull group by downtime'
               ' order by downtime desc limit %i;' % lastnum)
        self._query(sql, 'download-time, count # last %i records' % lastnum)
        print('-' * 79)

        return True

    def watch(self, limit=None):
        '''按观看次数排序'''
        if limit is None:
            sql = 'select * from bbvc order by playnum desc;'
        else:
            sql = ('select %s from bbvc where playnum >= %i'
                   ' order by playnum desc' % (self.columns, limit))
        return self._query(sql)

    def dm(self, limit=None):
        '''按弹幕数量排序'''
        if limit is None:
            sql = 'select * from bbvc order by dmnum desc;'
        else:
            sql = ('select %s from bbvc where dmnum >= %i'
                   ' order by dmnum desc' % (self.columns, limit))
        return self._query(sql)


# Main
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', action='store_true',
                        help='show all vc records')
    parser.add_argument('-s', nargs='?', const=5, type=int,
                        help='show overview report and last [5] records')
    parser.add_argument('-n', action='store',
                        help='search title name')
    parser.add_argument('-w', action='store', type=int,
                        help='sort by play number')
    parser.add_argument('-dm', action='store', type=int,
                        help='sort by danmu number')
    parser.add_argument('-p', action='store', nargs='?', const='all',
                        help='search by palace time')
    parser.add_argument('-d', action='store', nargs='?', const='all',
                        help='search by download time')
    parser.add_argument('-ul', action='store', nargs='?', const='all',
                        help='search by upload time')
    parser.add_argument('-ud', action='store', nargs='?', const='all',
                        help='search by update time')
    args = parser.parse_args()

    db = queryDB(db_file)
    if args.a:
        db.all()
    elif args.s is not None:
        db.statistics(args.s)
    elif args.n:
        db.name('%' + args.n + '%')
    elif args.w:
        db.watch(args.w)
    elif args.dm:
        db.dm(args.dm)
    elif args.d:
        db.download() if args.d == 'all' else db.download('%' + args.d + '%')
    elif args.p:
        db.palace() if args.p == 'all' else db.palace('%' + args.p + '%')
    elif args.ul:
        db.upload() if args.ul == 'all' else db.upload('%' + args.ul + '%')
    elif args.ud:
        db.update() if args.ud == 'all' else db.update('%' + args.ud + '%')
    else:
        print(parser.print_help())

    # db.avid('av44%')
    # db.upload('2017%')
    # db.palace()
    # db.download()
    # db.update()
    # db.dm(10000)

# End
