#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
@author: bo
@file: manage.py 
@version:
@time: 2019/11/06
@function： 运行flask
"""
from cookiespool.api import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
