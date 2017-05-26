#!/usr/bin/env python
# coding:utf-8
'''unit test for vc_db_tools.py'''

import test as tools

db = tools.queryDB('vc_data.db')


def test_query_all():
    rows = db.all()
    assert len(rows) > 1000


def test_query_stat():
    rows = db.statistics()
    assert rows is True


def test_query_name():
    rows = db.name(u'%神经病%')
    # print r
    assert type(rows) is list
    assert type(rows[0]) is tuple
    assert len(rows) > 0
    assert len(rows[0]) == 9


def test_query_watch():
    rows = db.watch(1000000)
    assert len(rows) > 15
    assert len(rows[10]) == 9


def test_query_dm():
    rows = db.dm(100000)
    assert len(rows) > 2
    assert len(rows[1]) == 9


def test_query_palace():
    rows = db.palace('%2017-05-08%')
    assert len(rows) > 2
    assert len(rows[1]) == 9

    rows = db.palace()
    assert len(rows) > 10


def test_query_upload():
    rows = db.upload('%2014-02-05%')
    assert len(rows) > 2
    assert len(rows[1]) == 9

    rows = db.upload()
    assert len(rows) > 700


def test_query_update():
    rows = db.update()
    assert len(rows) > 2


def test_query_download():
    rows = db.download('%2017-05-16%')
    assert len(rows) > 1
    assert len(rows[1]) == 9

    rows = db.download()
    assert len(rows) > 3


if __name__ == '__main__':
    test_query_name()
