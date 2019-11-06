import json
from flask import Flask, g
from cookiespool.db import *

__all__ = ['app']

app = Flask(__name__)


@app.route('/')
def index():
    return '<h2>Welcome to Cookie Pool System</h2>'


# @app.route('/<website>/random')
# def random(website):
#     """
#     获取随机的Cookie, 访问地址如 /weibo/random
#     :return: 随机Cookie
#     """
#     g = get_conn()
#     cookies = getattr(g, website + '_cookies').random()
#     return cookies


@app.route('/<website>/random')
def random(website):
    """
    获取随机的Cookie, 访问地址如 /weibo/random
    :return: 随机Cookie
    """
    g = get_conn()
    try:
        usernames = getattr(g, website + '_cookies').usernames()  # 取出所有key值
    except AttributeError:
        return json.dumps({'status': '2', 'message': 'There are no cookies in this website'})
    if usernames:
        username = usernames[0]
        cookies = getattr(g, website + '_cookies').get(username)
        getattr(g, website + '_cookies').delete(username)
        return json.dumps({'status:': '1', 'cookies': cookies})
    else:
        return json.dumps({'status': '2', 'message': 'There are no cookies in Cookie Pool'})


@app.route('/<website>/add/<username>/<password>')
def add(website, username, password):
    """
    添加用户, 访问地址如 /weibo/add/user/password
    :param website: 站点
    :param username: 用户名
    :param password: 密码
    :return: 
    """
    g = get_conn()
    print(username, password)
    try:
        getattr(g, website + '_accounts').set(username, password)
    except AttributeError:
        return json.dumps({'status': '2', 'message': 'You have to add infomations of this website'})
    return json.dumps({'status': '1'})


@app.route('/<website>/count')
def count(website):
    """
    获取Cookies总数
    """
    g = get_conn()
    try:
        count = getattr(g, website + '_cookies').count()
    except AttributeError:
        return json.dumps({'status': '2', 'message': 'There are no cookies in this website'})
    return json.dumps({'status': '1', 'count': count})


if __name__ == '__main__':
    app.run(port=8888)
    # 鬼晓得这是什么操作，自己调，搞不懂了，哈哈    只有你的6000起不来    8888  9999都可以
    # app.run()
