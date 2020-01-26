# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/25 22:33
# IDE：PyCharm

from app.blueprint.RenderForm import RenderForm
from wtforms import StringField, SubmitField, HiddenField

class FileForm(RenderForm):
    id = HiddenField("id")
    file_select = StringField("上传文件", render_kw={"type":"file"})
    file_submit = SubmitField("上传", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})