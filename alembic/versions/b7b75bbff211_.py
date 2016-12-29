"""empty message

Revision ID: b7b75bbff211
Revises: 77d87204b45a
Create Date: 2016-12-30 03:33:51.079466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7b75bbff211'
down_revision = '77d87204b45a'
branch_labels = None
depends_on = None

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('timelapses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('units', sa.Enum('h', 'd', 'w', 'm', 'y', name='unitenum'), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('progress', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.drop_table('timelapse')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('timelapse',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('title', sa.VARCHAR(length=64), nullable=False),
    sa.Column('units', sa.VARCHAR(length=1), nullable=False),
    sa.Column('duration', sa.INTEGER(), nullable=False),
    sa.Column('start_time', sa.DATETIME(), nullable=False),
    sa.Column('progress', sa.INTEGER(), nullable=False),
    sa.CheckConstraint("units IN ('h', 'd', 'w', 'm', 'y')", name='unitenum'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.drop_table('timelapses')
    ### end Alembic commands ###
