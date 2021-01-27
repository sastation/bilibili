#!/usr/bin/env python3

import os
import sys
import json

__path = os.path.dirname(__file__)
sys.path.append(__path)

# import private models
import exception, utils
from utils import Verify, Get, Post

headers = utils.default_headers
apis = utils.get_apis()

class VideoInfo():
    '''获取视频相关信息'''
    def __init__(self, verify: Verify=Verify()):
        if type(verify) != utils.Verify:
            raise exception.bilibiliApiException("请传入Verify类")
        else:
            self.verify = verify

    def get_info(self, bvid, is_simple=False):
        if is_simple:
            api = apis["video"]["info"]["info_simple"]                                                                                                  
        else:
            api = apis["video"]["info"]["info_detail"]

        params = { "bvid": bvid }
        if self.verify.has_sess():
            get = Get(url=api["url"], params=params, cookies=self.verify.get_cookies())
        else:
            get = Get(url=api["url"], params=params)
        
        return(get())

    def search_video(self, keyword="VOCALOID中文曲", page=1, order="click", search_type="video"):
        api = apis["other"]["search"]

        params = {"page": page, "keyword": keyword, "order": order, "search_type": search_type}
        if self.verify.has_sess():
            get = Get(url=api["url"], params=params, cookies=self.verify.get_cookies())
        else:
            get = Get(url=api["url"], params=params)

        return(get())

if __name__ == "__main__":
    print("test.py")
    print(__path)

    verify = Verify("False", "False")
    video = VideoInfo(verify)

    info = video.get_info(bvid="BV1ox4113732")
    print(json.dumps(info, indent=4, ensure_ascii=False))

    #items = video.search_video("VOCALOID中文曲", 30)
    #print(json.dumps(items, indent=4, ensure_ascii=False))
