#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: bo
@file: func.py
@version:
@time: 2019/11/01
@function： 爬虫cookie测试
"""
import requests
import random
import datetime
import time
import hashlib


class NewRankTest:
    def __init__(self, cookies):
        self.session = requests.session()

        self.headers = {
            'cookie': cookies,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
        }

    def non(self):
        li = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
        nonce = ''.join(li[random.randint(0, 15)] for _ in range(9))
        # print('nonce参数值', nonce)
        return nonce

    def md5(self, parm):
        hl = hashlib.md5()
        hl.update(parm.encode(encoding='utf-8'))
        sign = hl.hexdigest()
        # print('md5加密', sign)
        return sign

    def start(self, url):
        # keyword = json.loads(task.decode("utf-8"))['品牌中文名']
        key_list = ['中航健身会', '佰富', '马天奴', '红裳']
        keyword = key_list[random.randint(0, 3)]
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(now, "==>", '品牌:', keyword)

        key = "/xdnphb/data/weixinuser/searchWeixinDataByCondition?AppKey=joker&"

        nonce = self.non()
        data = {
            'filter': '',
            'hasDeal': 'false',
            'keyName': keyword,  # 中航健身会,佰富,马天奴,红裳
            'order': 'relation',
            'nonce': nonce,
        }
        signature = key + "&".join(f"{k}={v}" for k, v in data.items())
        signature_encode = self.md5(signature)
        data.update({"xyz": signature_encode})
        # url = "https://www.newrank.cn/xdnphb/data/weixinuser/searchWeixinDataByCondition"
        response = self.session.post(url, data=data, headers=self.headers)
        # print('返回数据：',response.text)
        if response.status_code == 200:
            return True

        else:
            return False
