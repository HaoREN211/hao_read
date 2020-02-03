# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/25 20:18
# IDE：PyCharm

from app import db
from app.blueprint.main import bp
from app.models.Pdf import Pdf, PostView
from app.models.Post import Post
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user
from app.blueprint.form_tools import (DeleteForm, flash_form_errors, create_db_row,  modify_db,
                                      modify_form_constructor, modify_upload, upload_form_constructor)
from app.blueprint.main.forms.pdf import PdfModifyForm, PdfCreateForm, PostForm
from datetime import datetime
from app.blueprint.main.forms.file import FileForm
from flask_login import login_required
from operator import and_

@bp.route('/index', methods=['GET', 'POST'])
@bp.route("/", methods=['GET', 'POST'])
def index():
    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))
    page = request.args.get('page', 1, type=int)
    items = Pdf.query.order_by().paginate(page, 10, False)

    add_form = PdfCreateForm()
    delete_form = DeleteForm()
    temp_error_form = None
    temp_modify_form = PdfModifyForm()
    temp_upload_form = FileForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if temp_upload_form.file_submit.data and temp_upload_form.validate_on_submit():
                current_file = request.files['file_select']
                saved_path = modify_upload(current_file, temp_upload_form, "pdfs")
                current_pdf = Pdf.query.get(int(temp_upload_form.id.data))
                current_pdf.link = saved_path
                flash("上传成功")
                return redirect(url_for("main.index"))
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    create_info = create_db_row(add_form, Pdf(), "main.index")
                    current_pdf = Pdf.query.order_by(Pdf.id.desc()).first()
                    current_pdf.create_user_id = current_user.id
                    return create_info
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    modify_info = modify_db(temp_modify_form, Pdf, 'main.index')
                    current_pdf = Pdf.query.get(int(temp_modify_form.id.data))
                    current_pdf.update_time = datetime.now()
                    return modify_info
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = Pdf.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("main.index"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("main.index"))
    modify_form = modify_form_constructor(items, "PdfModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    upload_form = upload_form_constructor(items)

    next_url = url_for('main.index', page=items.next_num) if items.has_next else None
    prev_url = url_for('main.index', page=items.prev_num) if items.has_prev else None

    return render_template("main/index.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form,
                           upload_form=upload_form)


@bp.route('/index/<id>', methods=['GET', 'POST'])
@login_required
def index_id(id):
    current_pdf = Pdf.query.get(int(id))
    post_form = PostForm()

    # 新增用户浏览
    view_cnt = PostView.query.filter(and_(and_(PostView.user_id==current_user.id,
                                          PostView.pdf_id==id),
                                          PostView.view_date==datetime.now().date())).count()
    if view_cnt == 0:
        new_view = PostView(
            user_id=current_user.id,
            pdf_id=id,
            view_date=datetime.now().date()
        )
        db.session.add(new_view)
    # current_pdf.user_view_pdf(current_user.id)


    # 如果用户在该pdf上还没创建评论的话则创建
    if not current_pdf.user_has_post(current_user.id):
        new_post = Post(user_id=int(current_user.id),
                        pdf_id=int(id))
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("main.index_id", id=id))

    # 提交表单修改笔记内容时
    if post_form.post_submit.data and post_form.validate_on_submit():
        print(post_form.id.data)
        current_post = Post.query.get(post_form.id.data)
        if current_post.body == post_form.body.data:
            flash("无任何修改")
        else:
            current_post.body = post_form.body.data
            current_post.update_time = datetime.now()
            flash("修改成功")
        return redirect(url_for("main.index_id", id=id))

    current_post_id = current_pdf.get_user_post_id(current_user.id)
    current_post = Post.query.get(current_post_id)
    post_form.id.data = current_post.id
    post_form.body.data = current_post.body

    return render_template("main/pdf.html", pdf=current_pdf, post=post_form)