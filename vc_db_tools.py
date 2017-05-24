#!/usr/bin/env python
# coding: utf-8
'''
用于对vc数据库进行查询的一组工具
'''
import sqlite3
import argparse
import time

db_file = 'vc_data.db'


class queryDB(object):
    '''查询DB工具类'''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.one_week_ago = time.strftime('%Y-%m-%d',
                                          time.localtime(time.time() - 24 * 3600 * 7))

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
                   ' from bbvc where palacetime like "%s"'
                   ' order by palacetime;' % day)
            self._query(sql)

    def download(self, day=None):
        if day is None:
            sql = 'select downtime, count(*) from bbvc group by downtime;'
            self._query(sql, 'download-time, count')
        else:
            sql = ('select avnum, uploadtime, updatetime, palacetime,'
                   ' downtime, downstatus, playnum, dmnum, title'
                   ' from bbvc where downtime like "%s"'
                   ' order by downtime;' % day)
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

    def statistics(self, lastnum=7):
        '''overview report and last <lastnum> records'''
        sql = 'select count(*) from bbvc;'
        self._query(sql, 'Total')
        print '-' * 79

        sql = 'select count(*) from bbvc where updatetime isnull;'
        self._query(sql, 'none-updatime-count')
        sql = ('select count(*) from bbvc where updatetime notnull;')
        self._query(sql, 'update-count')
        sql = ('select updatetime, count(*) from bbvc'
               ' where updatetime notnull group by updatetime'
               ' order by updatetime desc limit %i;' % lastnum)
        self._query(sql, 'update-time, count # last %i records' % lastnum)
        print '-' * 79

        sql = 'select count(*) from bbvc where palacetime isnull;'
        self._query(sql, 'none-palace-count')
        sql = ('select count(*) from bbvc where palacetime notnull;')
        self._query(sql, 'palace-count')
        sql = ('select palacetime, count(*) from bbvc'
               ' where palacetime notnull group by palacetime'
               ' order by palacetime desc limit %i;' % lastnum)
        self._query(sql, 'palace-time, count # last %i records' % lastnum)
        print '-' * 79

        sql = 'select count(*) from bbvc where downtime isnull;'
        self._query(sql, 'none-download-count')
        sql = ('select count(*) from bbvc where downtime notnull;')
        self._query(sql, 'download-count')
        sql = ('select downtime, count(*) from bbvc'
               ' where downtime notnull group by downtime'
               ' order by downtime desc limit %i;' % lastnum)
        self._query(sql, 'download-time, count # last %i records' % lastnum)
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
    parser.add_argument('-s', '--stat', nargs='?', const=5, type=int,
                        help='show overview report and last [5] records')
    parser.add_argument('-n', '--name', action='store',
                        help='search title name')
    parser.add_argument('-w', '--watch', action='store', type=int,
                        help='sort by play number')
    parser.add_argument('-dm', '--danmu', action='store', type=int,
                        help='sort by danmu number')
    parser.add_argument('-p', '--palace', action='store',
                        help='search by palace time')
    parser.add_argument('-d', '--download', action='store',
                        help='search by download time')
    parser.add_argument('-ul', '--upload', action='store',
                        help='search by upload time')
    parser.add_argument('-ud', '--update', action='store',
                        help='search by update time')
    args = parser.parse_args()

    db = queryDB(db_file)
    if args.all:
        db.all()
    elif args.stat >= 0:
        db.statistics(args.stat)
    elif args.name:
        db.name('%' + args.name + '%')
    elif args.watch:
        db.watch(args.watch)
    elif args.danmu:
        db.dm(args.danmu)
    elif args.download:
        if args.download == 'all':
            db.download()
        else:
            db.download('%' + args.download + '%')
    elif args.palace:
        if args.palace == 'all':
            db.palace()
        else:
            db.palace('%' + args.palace + '%')
    elif args.upload:
        if args.upload == 'all':
            db.upload()
        else:
            db.upload('%' + args.upload + '%')
    elif args.update:
        if args.update == 'all':
            db.update()
        else:
            db.update('%' + args.update + '%')
    else:
        print parser.print_help()

    # db.avid('av44%')
    # db.upload('2017%')
    # db.palace()
    # db.download()
    # db.update()
    # db.dm(10000)

# End
