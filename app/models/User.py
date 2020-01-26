# 作者：hao.ren3
# 时间：2019/11/7 15:42
# IDE：PyCharm
from app import login
from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.mysql import BIGINT


user_group = db.Table('user_group',
    db.Column('id',
              BIGINT(unsigned=True),
              primary_key=True,
              comment='用户所属组主键'),
    db.Column('user_id',
              BIGINT(unsigned=True),
              db.ForeignKey('user.id'),
              comment='用户'),
    db.Column('group_id',
              BIGINT(unsigned=True),
              db.ForeignKey('group.id'),
              comment='用户组'),
    db.UniqueConstraint('user_id', 'group_id',
              name='user_group_unique_constraint'),
    comment='用户-用户组'
)


class User(UserMixin, db.Model):
    __table_args__ = {'comment': '用户信息'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment='用户主键')
    username = db.Column(db.String(64), index=True, unique=True, comment='用户账号名')
    profile_name = db.Column(db.String(64), index=True, comment='用户昵称')
    email = db.Column(db.String(120), index=True, unique=True, comment='用户邮箱地址')
    about_me = db.Column(db.Text, comment='关于我的个人简介')
    last_seen = db.Column(db.DateTime, default=datetime.now(), comment='用户最后一次登录时间')
    password_hash = db.Column(db.String(128), comment='用户密码')
    real_name = db.Column(db.String(128), comment='用户真实姓名')
    is_admin = db.Column(db.Boolean, comment='是否是超级管理员', default=False)

    create_time = db.Column(db.DateTime, default=datetime.now(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now(), comment="更新时间")

    groups = db.relationship(
        'Group', secondary=user_group,
        primaryjoin=(user_group.c.user_id == id),
        secondaryjoin=(user_group.c.group_id == id),
        backref=db.backref('users', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Group(db.Model):
    __table_args__ = {'comment': '用户组'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment='用户组主键')
    name = db.Column(db.String(100), nullable=False, comment="分组名", unique=True)

    create_user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("user.id"), comment='创建用户')
    create_time = db.Column(db.DateTime, default=datetime.now(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now(), comment="更新时间")


