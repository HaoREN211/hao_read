# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/25 21:05
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT
from datetime import datetime
from operator import and_
from app.models.User import User


pdf_group = db.Table('pdf_group',
    db.Column('id',
              BIGINT(unsigned=True),
              primary_key=True,
              comment='PDF所属组主键'),
    db.Column('pdf_id',
              BIGINT(unsigned=True),
              db.ForeignKey('pdf.id'),
              comment='PDF'),
    db.Column('group_id',
              BIGINT(unsigned=True),
              db.ForeignKey('group.id'),
              comment='用户组'),
    db.UniqueConstraint('pdf_id', 'group_id',
              name='pdf_group_unique_constraint'),
    comment='PDF-用户组'
)



post_view = db.Table(
    'post_view',
    db.Column('id',
              BIGINT(unsigned=True),
              primary_key=True,
              comment='用户查看pdf主键'),
    db.Column('user_id',
              BIGINT(unsigned=True),
              db.ForeignKey('user.id'),
              comment='用户'),
    db.Column('pdf_id',
              BIGINT(unsigned=True),
              db.ForeignKey('pdf.id'),
              comment='PDF'),
    db.Column('view_date',
              db.Date,
              default=datetime.now(),
              comment="浏览事件"),
    db.UniqueConstraint("user_id", "pdf_id", "view_date", name="unique_constrain_user_view_pdf"),
    comment="用户浏览pdf记录"
)


class Pdf(db.Model):
    __table_args__ = {'comment': 'PDF信息'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment='PDF主键')

    name = db.Column(db.String(100), nullable=False, comment="PDF书名")
    link = db.Column(db.String(500), nullable=True, comment="PDF链接")
    end_date = db.Column(db.Date, nullable=True, comment="时间截点")

    create_user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("user.id"), comment='创建用户')
    create_time = db.Column(db.DateTime, default=datetime.now(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now(), comment="更新时间")

    groups = db.relationship(
        'Group', secondary=pdf_group,
        primaryjoin=(pdf_group.c.pdf_id == id),
        secondaryjoin=(pdf_group.c.group_id == id),
        backref=db.backref('pdfs', lazy='dynamic'), lazy='dynamic')

    viewers = db.relationship(
        'User', secondary=post_view,
        lazy="dynamic")

    # 判断用户当日是否浏览了帖子
    def user_has_viewed_pdf(self, user_id):
        return self.viewers.filter(and_(
            post_view.c.user_id == int(user_id),
            post_view.c.view_date == datetime.now().date()
        )).count()>0

    # 用户浏览pdf事件
    def user_view_pdf(self, user_id):
        if not self.user_has_viewed_pdf(user_id):
            current_user = User.query.get(int(user_id))
            self.viewers.append(current_user)

    # 判断用户user_id在该pdf上是否创建了评论
    def user_has_post(self, user_id):
        return len(list(filter(lambda x:x.user_id==int(user_id), self.posts)))>0

    # 获取用户在该pdf上的评论主键
    def get_user_post_id(self, user_id):
        if self.user_has_post(user_id):
            for current_post in self.posts:
                if current_post.user_id == int(user_id):
                    return current_post.id
        return 0