# 作者：hao.ren3
# 时间：2019/11/7 15:44
# IDE：PyCharm
from datetime import datetime
from app import db
from sqlalchemy.dialects.mysql import BIGINT

class Post(db.Model):
    __table_args__ = (db.UniqueConstraint("user_id", "pdf_id", name="unique_constraint_user_pdf"), )
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment='帖子主键')
    body = db.Column(db.Text(16777216), comment='帖子内容')

    user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('user.id'), comment='帖子作者的用户ID')
    pdf_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('pdf.id'), comment='帖子作者的用户ID')

    create_time = db.Column(db.DateTime, index=True, default=datetime.now(), comment='帖子创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now(), comment="更新时间")

    pdf = db.relationship("Pdf", backref="posts", foreign_keys=[pdf_id])

