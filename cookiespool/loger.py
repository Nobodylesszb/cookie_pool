#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
@author: bo
@file: loger.py 
@version:
@time: 2019/11/05
@function：日志系统
"""
# !/usr/bin/python
# -*- coding: utf-8 -*-
""" 
@author: bo
@file: log_file.py.py 
@version:
@time: 2019/07/25
@function： 
"""
import os
import datetime
import logging
import logging.handlers


class LogMgr:
    def __init__(self, logFile):
        self._logger = logging.getLogger("logger")
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_dir = r"..\..\logs\generator\{date}".format(date=date)
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        log_filename = log_dir + '/' + logFile

        handler = logging.FileHandler(log_filename)
        formatter = logging.Formatter(
            '%(asctime)s %(funcName)s [line:%(lineno)d]  %(levelno)s %(levelname)s  threadID:%(thread)d threadName:%(threadName)s msg:%(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)

    def error(self, msg):
        if self._logger is not None:
            self._logger.error(msg)

    def info(self, msg):
        if self._logger is not None:
            self._logger.info(msg)

    def debug(self, msg):
        if self._logger is not None:
            self._logger.debug(msg)

    def mark(self, msg):
        if self._logger is not None:
            self._logger.info(msg)


def main():
    global log_mgr
    log_mgr = LogMgr("2017")
    log_mgr.error('[mylog]This is error log')
    log_mgr.info('[mylog]This is info log')
    log_mgr.debug('[mylog]This is debug log')
    log_mgr.mark('[mymark]This is mark log')


if __name__ == "__main__":
    main()
