"""empty message

Revision ID: 8b2910381c28
Revises: a7fedcb2a3b9
Create Date: 2020-01-25 20:56:51.380725

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8b2910381c28'
down_revision = 'a7fedcb2a3b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_group',
    sa.Column('id', mysql.BIGINT(unsigned=True), nullable=False, comment='用户所属组主键'),
    sa.Column('user_id', mysql.BIGINT(unsigned=True), nullable=True, comment='用户'),
    sa.Column('group_id', mysql.BIGINT(unsigned=True), nullable=True, comment='用户组'),
    sa.Column('create_user_id', mysql.BIGINT(unsigned=True), nullable=True, comment='创建用户'),
    sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.ForeignKeyConstraint(['create_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    comment='用户所属组'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_group')
    # ### end Alembic commands ###