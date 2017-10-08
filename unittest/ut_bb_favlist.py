#!/usr/bin/env python
# coding:utf-8
'''
Author: David Wang
Date: 2017.08.03
Purpose: unit test for bb_favlist.py
Usage: pytest3 unittest/ut_bb_favlist.py
'''

import os
import sys

lastdir = os.path.split(os.getcwd())[-1]

if lastdir == 'unittest':
    path = '..'
else:
    path = '.'


if path:
    sys.path.append(path)
    import bb_favlist as space


mid = '25527367'
fid = '35011734'  # 'VC之家'


def test_sidebar():
    rows = space.get_sidebar(mid)
    assert len(rows) > 1
    assert rows[0]['name'] == u'默认收藏夹'


def test_favorite():
    pages, favlist = space.get_favorite(mid, fid, 1)
    assert len(favlist) > 1
    assert pages > 2


def test_all_favorite():
    favlist = space.get_all_favlist(mid, fid)
    assert len(favlist) > 50


if __name__ == '__main__':
    test_sidebar()
