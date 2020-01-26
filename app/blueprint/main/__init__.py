# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/25 20:18
# IDE：PyCharm


from flask import Blueprint

bp = Blueprint('main', __name__)

from app.blueprint.main.routes import index
