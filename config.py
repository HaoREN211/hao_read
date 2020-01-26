# 作者：hao.ren3
# 时间：2019/11/5 16:35
# IDE：PyCharm

import os
from config_db import ConfigDb


class Config(object):
    # 分页功能，每页显示的个数
    POSTS_PER_PAGE = 10

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-hao-guess'
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = ConfigDb.USERNAME
    PASSWORD = ConfigDb.PASSWORD
    HOST = ConfigDb.HOST
    PORT = ConfigDb.PORT
    DATABASE = ConfigDb.DATABASE
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 5

    SQLALCHEMY_POOL_TIMEOUT = 10

    # 设置多少秒后回收连接，在使用 MySQL 时是必须设置的。
    SQLALCHEMY_POOL_RECYCLE = 10

    BOOTSTRAP_SERVE_LOCAL = True


class TranslateForm(object):
    class Login(object):
        Username = "账号"
        Password = "密码"
        PageTitle = "请登录"
        RememberMe = "请记住我"
        submit = "登录"
        register = "注册"

    class TranslatePage(object):
        Home = "主页"
        Login = "登录"

    class ChineseLanguage:
        class Profile:
            edit_profile = "修改资料"
            saved = "资料修改成功"
            profile = "用户资料"