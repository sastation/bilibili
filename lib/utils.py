import json
import datetime
import time
import os
import sys
import requests
import base64
import urllib3
import logging

urllib3.disable_warnings()

__path = os.path.dirname(__file__)

# import private models
sys.path.append(__path)
import exception 

default_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/79.0.3945.130 Safari/537.36",
    "Referer": "https://www.bilibili.com"
}

logger = logging.getLogger("bilibili_api")
logger.setLevel(logging.WARNING)
logger.addHandler(logging.StreamHandler())


def get_apis():
    with open(os.path.join(__path, "api.json"), "r", encoding="utf-8") as f:
        apis = json.loads(f.read())
        f.close()
    return apis


class Verify:
    '''用于用户身份验证'''
    def __init__(self, sessdata: str = "False", csrf: str = "False"):
        self.sessdata = sessdata
        self.csrf = csrf

    def get_cookies(self):
        cookies = {
            "SESSDATA": self.sessdata
        }
        return cookies

    def has_sess(self):
        if self.sessdata != "False":
            return True
        else:
            return False

    def has_csrf(self):
        if self.csrf != "False":
            return True
        else:
            return False

    def check(self):
        ret = {
            "code": -2,
            "message": ""
        }
        if not self.has_sess():
            ret["code"] = -3
            ret["message"] = "未提供SESSDATA"
        else:
            api = "https://api.bilibili.com/x/web-interface/archive/like"
            data = {"aid": "83175485", "like": 1, "csrf": self.csrf}
            req = requests.post(url=api, data=data, cookies=self.get_cookies())
            if req.ok:
                con = req.json()
                if con["code"] == -111:
                    ret["code"] = -1
                    ret["message"] = "csrf 校验失败"
                elif con["code"] == -101 or con["code"] == -400:
                    ret["code"] = -2
                    ret["message"] = "SESSDATA值有误"
                else:
                    ret["code"] = 0
                    ret["message"] = "0"
            else:
                raise exception.NetworkException(req.status_code)
        return ret


class Get:
    def __init__(self, url, params=None, cookies=None, headers=None):
        if headers is None:
            self.headers = default_headers
        else:
            self.headers = headers
        if cookies is None:
            self.cookies = {}
        else:
            self.cookies = cookies
        if params is None:
            self.params = {}
        else:
            self.params = params
        self.url = url

    def __call__(self):
        req = requests.get(url=self.url, params=self.params, headers=self.headers, cookies=self.cookies, verify=False)
        if req.ok:
            con = json.loads(req.text)
            if con["code"] != 0:
                raise exception.BiliException(con["code"], con["message"])
            else:
                return con["data"]
        else:
            raise exception.NetworkException(req.status_code)


class Post:
    def __init__(self, url, cookies, data=None, headers=None):
        if headers is None:
            self.headers = default_headers
        else:
            self.headers = headers
        if cookies is None:
            self.cookies = {}
        else:
            self.cookies = cookies
        if data is None:
            self.data = {}
        else:
            self.data = data
        self.url = url

    def __call__(self):

        req = requests.post(url=self.url, data=self.data, headers=self.headers, cookies=self.cookies, verify=False)
        if req.ok:
            con = json.loads(req.text)
            if con["code"] != 0:
                raise exception.BiliException(con["code"], con["message"])
            else:
                return con
        else:
            raise exception.NetworkException(req.status_code)


# 代码来源：https://www.zhihu.com/question/381784377/answer/1099438784
def bv2aid(bv: str):
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr = {}
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608

    def dec(x):
        r = 0
        for i in range(6):
            r += tr[x[s[i]]] * 58 ** i
        return (r - add) ^ xor

    return dec(bv)


# 代码来源：https://www.zhihu.com/question/381784377/answer/1099438784
def aid2bv(aid: int):
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr = {}
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608

    def enc(x):
        x = (x ^ xor) + add
        r = list('BV1  4 1 7  ')
        for i in range(6):
            r[s[i]] = table[x // 58 ** i % 58]
        return ''.join(r)

    return enc(aid)


if __name__ == "__main__":
    print("Main")
    print(__path)
    print(get_apis()['other'])
