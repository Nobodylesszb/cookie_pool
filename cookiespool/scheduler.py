from multiprocessing import Process
from cookiespool.api import app
from cookiespool.config import *
from cookiespool.generator import *
from cookiespool.tester import *
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

import datetime
import logging

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=r'C:\Users\Administrator\Desktop\CookiesPool-master\logs\schedule\schedule.txt',
                    filemode='a')
scheduler = BlockingScheduler()
back_scheduler = BackgroundScheduler()


def my_listener(event):
    if event.exception:
        print('任务出错了！！！！！！')
    else:
        print('任务照常运行...')


class Scheduler(object):
    # @staticmethod
    # def valid_cookie():
    #     # while True:
    #     print('Cookies检测进程开始运行')
    #     try:
    #         for website, cls in TESTER_MAP.items():
    #             tester = eval(cls + '(website="' + website + '")')
    #             tester.run()
    #             print('Cookies检测完成')
    #             del tester
    #     except Exception as e:
    #         print(e.args)
    #
    @staticmethod
    def valid_cookie():
        # while True:
        print('Cookies检测进程开始运行')
        try:
            for website, cls in TESTER_MAP.items():
                tester = eval(cls + '(website="' + website + '")')
                tester.run()
                print('Cookies检测完成')
                del tester
        except Exception as e:
            print(e.args)

    @staticmethod
    def generate_cookie():
        print('Cookies生成进程开始运行')
        try:
            for website, cls in GENERATOR_MAP.items():
                generator = eval(cls + '(website="' + website + '")')
                generator.run()
                print('Cookies生成完成')
                generator.close()

        except Exception as e:
            print(e.args)

    @staticmethod
    def schedule_generate_cookie():
        """
        定时生成cookie任务
        :return:
        """
        back_scheduler.add_job(func=Scheduler.generate_cookie, trigger='cron', hour='1')
        back_scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        back_scheduler._logger = logging
        back_scheduler.start()

    @staticmethod
    def schedule_valid_cookie():
        """
        定时检测cookie任务
        :return:
        """
        back_scheduler.add_job(func=Scheduler.valid_cookie, trigger='cron', hour='4', )
        # back_scheduler.add_job(func=Scheduler.valid_cookie, trigger='interval', seconds='10',
        #                        next_run_time=datetime.datetime.now())
        back_scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        back_scheduler._logger = logging
        back_scheduler.start()

    @staticmethod
    def api():
        print('API接口开始运行')
        app.run(debug=True, host=API_HOST, port=API_PORT)

    def run(self):
        if API_PROCESS:
            api_process = Process(target=Scheduler.api)
            api_process.start()

        if GENERATOR_PROCESS:
            generate_process = Process(target=Scheduler.schedule_generate_cookie)
            generate_process.start()

        if VALID_PROCESS:
            valid_process = Process(target=Scheduler.schedule_valid_cookie)
            valid_process.start()


if __name__ == '__main__':
    s = Scheduler()
    s.run()
