#!/usr/bin/env python
# coding: utf-8
'''
用于对vc数据库进行查询的一组工具
'''
import sqlite3
import argparse

db_file = 'vc_data.db'


class queryDB(object):
    '''查询DB工具类'''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)

    def __del__(self):
        self.conn.close()

    def _query(self, sql, title=None):
        if title is None:
            print ('avnum, upload-time, update-time, palace-time,'
                   ' download-time, download-status, watch-times,'
                   ' dm-times, title')
        else:
            print title

        curs = self.conn.execute(sql)
        rows = curs.fetchall()
        for row in rows:
            for item in row:
                if type(item) == unicode:
                    print item.encode('utf-8'),
                elif item is None:
                    print '-',
                else:
                    print item,
            print ""

    def all(self):
        sql = ('select avnum, uploadtime, updatetime, palacetime,'
               ' downtime, downstatus, playnum, dmnum, title'
               ' from bbvc;')
        self._query(sql)

    def avid(self, avnum='%'):
        sql = ('select avnum, uploadtime, updatetime, palacetime,'
               ' downtime, downstatus, playnum, dmnum, title'
               ' from bbvc where avnum like "%s";' % avnum)
        self._query(sql)

    def name(self, title='%'):
        sql = ('select avnum, uploadtime, updatetime, palacetime,'
               ' downtime, downstatus, playnum, dmnum, title'
               ' from bbvc where title like "%s";' % title)
        self._query(sql)

    def upload(self, day=None):
        if day is None:
            sql = 'select uploadtime, count(*) from bbvc group by uploadtime;'
            self._query(sql, 'uplaodtime, count')
        else:
            sql = ('select avnum, uploadtime, updatetime, palacetime,'
                   ' downtime, downstatus, playnum, dmnum, title'
                   ' from bbvc where uploadtime like "%s";' % day)
            self._query(sql)

    def palace(self, day=None):
        if day is None:
            sql = 'select palacetime, count(*) from bbvc group by palacetime;'
            self._query(sql, 'palace-time, count')
        else:
            sql = ('select avnum, uploadtime, updatetime, palacetime,'
                   ' downtime, downstatus, playnum, dmnum, title'
                   ' from bbvc where palacetime like "%s";' % day)
            self._query(sql)

    def download(self, day=None):
        if day is None:
            sql = 'select downtime, count(*) from bbvc group by downtime;'
            self._query(sql, 'download-time, count')
        else:
            sql = ('select avnum, uploadtime, updatetime, palacetime,'
                   ' downtime, downstatus, playnum, dmnum, title'
                   ' from bbvc where downtime like "%s";' % day)
            self._query(sql)

    def update(self, day=None):
        if day is None:
            sql = 'select updatetime, count(*) from bbvc group by updatetime;'
            self._query(sql, 'update-time, count')
        else:
            sql = ('select avnum, uploadtime, updatetime, palacetime,'
                   ' downtime, downstatus, playnum, dmnum, title'
                   ' from bbvc where updatetime like "%s";' % day)
            self._query(sql)

    def statistics(self):
        sql = 'select count(*) from bbvc;'
        self._query(sql, 'Total')
        print '-' * 79
        self.update()
        print '-' * 79
        self.palace()
        print '-' * 79
        self.download()
        print '-' * 79

    def watch(self, limit=None):
        if limit is None:
            sql = 'select * from bbvc order by playnum desc;'
        else:
            sql = ('select * from bbvc where playnum >= %i'
                   ' order by playnum desc' % limit)
        self._query(sql)

    def dm(self, limit=None):
        if limit is None:
            sql = 'select * from bbvc order by dmnum desc;'
        else:
            sql = ('select * from bbvc where dmnum >= %i'
                   ' order by dmnum desc' % limit)
        self._query(sql)


# Main
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--all', action='store_true',
                        help='show all vc records')
    parser.add_argument('-s', '--stat', action='store_true',
                        help='show overall report')
    parser.add_argument('-n', '--name', action='store',
                        help='search title name')
    parser.add_argument('-w', '--watch', action='store', type=int,
                        help='sort by play number')
    args = parser.parse_args()

    db = queryDB(db_file)
    if args.all:
        db.all()
    elif args.stat:
        db.statistics()
    elif args.name:
        db.name('%'+args.name+'%')
    elif args.watch:
        db.watch(args.watch)
    else:
        print parser.print_help()

    # db.avid('av44%')
    # db.upload('2017%')
    # db.palace()
    # db.download()
    # db.update()
    # db.dm(10000)

# End
