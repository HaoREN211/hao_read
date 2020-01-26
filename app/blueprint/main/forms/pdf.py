# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/25 21:59
# IDE：PyCharm

from app.models.Pdf import Pdf
from app.blueprint.RenderForm import RenderForm
from wtforms import StringField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length

class PdfCreateForm(RenderForm):
    name = StringField("名称", validators=[DataRequired(), Length(max=100, min=1)])
    link = StringField("链接", validators=[DataRequired(), Length(max=500, min=1)])
    end_date = StringField("时间截点", render_kw={"type":"date"})

    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_pdf = Pdf.query.filter_by(name=str(name.data).strip()).all()
        if list_pdf and (len(list_pdf) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')

class PdfModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称", validators=[DataRequired(), Length(max=100, min=1)])
    link = StringField("链接", validators=[DataRequired(), Length(max=500, min=1)])
    end_date = StringField("时间截点", render_kw={"type": "date"})

    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_pdf = Pdf.query.filter_by(name=str(name.data).strip()).all()
        if list_pdf and (len(list_pdf) > 0):
            list_id = [x.id for x in list_pdf]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')

class PostForm(RenderForm):
    id = HiddenField("主键")
    body = TextAreaField("我的笔记", validators=[Length(max=16777216)],
                         render_kw={"class":"form-control"})
    post_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})