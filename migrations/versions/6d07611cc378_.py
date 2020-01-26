"""empty message

Revision ID: 6d07611cc378
Revises: 95eb2674e0a3
Create Date: 2020-01-26 14:22:21.206594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d07611cc378'
down_revision = '95eb2674e0a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table_comment(
        'post_view',
        '用户浏览pdf记录',
        existing_comment=None,
        schema=None
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table_comment(
        'post_view',
        existing_comment='用户浏览pdf记录',
        schema=None
    )
    # ### end Alembic commands ###