import json
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from cookiespool.config import *
from cookiespool.db import RedisClient

from login.weibo.cookies import WeiboCookies
from login.newrank.cookies import NewRankCookies
import logging
from cookiespool.loger import LogMgr


# logging.basicConfig(level=logging.WARNING,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     filename='../cookiesPool-master/logs/generator/generator.txt',
#                     filemode='a')


class CookiesGenerator(object):
    def __init__(self, website='default'):
        """
        父类, 初始化一些对象
        :param website: 名称
        :param browser: 浏览器, 若不使用浏览器则可设置为 None
        """
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)
        self.init_browser()

    def __del__(self):
        self.close()

    def init_browser(self):
        """
        通过browser参数初始化全局浏览器供模拟登录使用
        :return:
        """
        if BROWSER_TYPE == 'PhantomJS':
            caps = DesiredCapabilities.PHANTOMJS
            caps[
                "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
            self.browser = webdriver.PhantomJS(desired_capabilities=caps)
            self.browser.set_window_size(1400, 500)
        elif BROWSER_TYPE == 'Chrome':
            self.browser = webdriver.Chrome()

    def new_cookies(self, username, password):
        """
        新生成Cookies，子类需要重写
        :param username: 用户名
        :param password: 密码
        :return:
        """
        raise NotImplementedError

    def process_cookies(self, cookies):
        """
        处理Cookies
        :param cookies:
        :return:
        """
        dict = {}
        for cookie in cookies:
            dict[cookie['name']] = cookie['value']
        return dict

    def run(self):
        """
        运行, 得到所有账户, 然后顺次模拟登录
        :return:
        """
        accounts_usernames = self.accounts_db.usernames()
        cookies_usernames = self.cookies_db.usernames()

        for username in accounts_usernames:
            if not username in cookies_usernames:
                password = self.accounts_db.get(username)
                print('正在生成Cookies', '账号', username, '密码', password)
                result = self.new_cookies(username, password)
                # 成功获取
                if result.get('status') == 1:
                    cookies = self.process_cookies(result.get('content'))
                    print('成功获取到Cookies', cookies)
                    if self.cookies_db.set(username, json.dumps(cookies)):
                        print('成功保存Cookies')
                # 密码错误，移除账号
                elif result.get('status') == 2:
                    print(result.get('content'))
                    if self.accounts_db.delete(username):
                        print('成功删除账号')
                else:
                    print(result.get('content'))
        else:
            print('所有账号都已经成功获取Cookies')

    def close(self):
        """
        关闭
        :return:
        """
        try:
            print('Closing Browser')
            self.browser.close()
            del self.browser
        except TypeError:
            print('Browser not opened')


class WeiboCookiesGenerator(CookiesGenerator):
    def __init__(self, website='weibo'):
        """
        初始化操作
        :param website: 站点名称
        :param browser: 使用的浏览器
        """
        CookiesGenerator.__init__(self, website)
        self.website = website

    def new_cookies(self, username, password):
        """
        生成Cookies
        :param username: 用户名
        :param password: 密码
        :return: 用户名和Cookies
        """
        return WeiboCookies(username, password, self.browser).main()


class NewRankCookiesGenerator(CookiesGenerator):
    def __init__(self, website='newrank'):
        """
        初始化操作
        :param website: 站点名称
        :param browser: 使用的浏览器
        """
        CookiesGenerator.__init__(self, website)
        self.website = website
        self.loger = LogMgr('{web}.txt'.format(web=self.website))

    def new_cookies(self, username, password):
        """
        生成Cookies
        :param username: 用户名
        :param password: 密码
        :return: 用户名和Cookies
        """
        return NewRankCookies(username, password).main()

    def run(self):
        """
        运行, 得到所有账户, 然后顺次模拟登录
        :return:
        """
        accounts_usernames = self.accounts_db.usernames()
        cookies_usernames = self.cookies_db.usernames()

        for username in accounts_usernames:
            if not username in cookies_usernames:
                password = self.accounts_db.get(username)
                print('正在生成Cookies', '账号', username, '密码', password)
                result = self.new_cookies(username, password)
                # 成功获取
                if result.get('status') == 1:
                    # cookies = self.process_cookies(result.get('content'))
                    cookies = result.get('content')
                    print('成功获取到Cookies', cookies)
                    if self.cookies_db.set(username, cookies):
                        print('成功保存Cookies')
                # 密码错误，移除账号
                elif result.get('status') == 2:
                    print(result.get('content'))
                    if self.accounts_db.delete(username):
                        print('成功删除账号')
                        self.loger.error(
                            '{website}----{name}账号因账号或密码错误已从redis中删除'.format(website=self.website, name=username))
                elif result.get('status') == 4:
                    print(result.get('content'))
                    if self.accounts_db.delete(username):
                        print('成功删除账号')
                        self.loger.error(
                            '{website}----{name}账号因账号被冻结已从redis中删除'.format(website=self.website, name=username))
                else:
                    self.loger.error(
                        '{website}----{name}账号因其他原因已从redis中删除'.format(website=self.website, name=username))
                    print(result.get('content'))
        else:
            print('所有账号都已经成功获取Cookies')


if __name__ == '__main__':
    generator = NewRankCookiesGenerator()
    generator.run()
