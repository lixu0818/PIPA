"""empty message

Revision ID: b8cfdf6208df
Revises: 
Create Date: 2017-03-17 20:42:04.374410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8cfdf6208df'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('username', sa.String(length=60), nullable=True),
    sa.Column('first_name', sa.String(length=60), nullable=True),
    sa.Column('last_name', sa.String(length=60), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
    sa.Column('lastmodified', sa.DateTime(timezone=True), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_first_name'), 'users', ['first_name'], unique=False)
    op.create_index(op.f('ix_users_last_name'), 'users', ['last_name'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('recommend_articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('source_pmid', sa.Integer(), nullable=True),
    sa.Column('entry_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('pmid_1', sa.Integer(), nullable=True),
    sa.Column('pmid_2', sa.Integer(), nullable=True),
    sa.Column('pmid_3', sa.Integer(), nullable=True),
    sa.Column('pmid_4', sa.Integer(), nullable=True),
    sa.Column('pmid_5', sa.Integer(), nullable=True),
    sa.Column('pmid_6', sa.Integer(), nullable=True),
    sa.Column('pmid_7', sa.Integer(), nullable=True),
    sa.Column('pmid_8', sa.Integer(), nullable=True),
    sa.Column('pmid_9', sa.Integer(), nullable=True),
    sa.Column('pmid_10', sa.Integer(), nullable=True),
    sa.Column('score_1', sa.Float(), nullable=True),
    sa.Column('score_2', sa.Float(), nullable=True),
    sa.Column('score_3', sa.Float(), nullable=True),
    sa.Column('score_4', sa.Float(), nullable=True),
    sa.Column('score_5', sa.Float(), nullable=True),
    sa.Column('score_6', sa.Float(), nullable=True),
    sa.Column('score_7', sa.Float(), nullable=True),
    sa.Column('score_8', sa.Float(), nullable=True),
    sa.Column('score_9', sa.Float(), nullable=True),
    sa.Column('score_10', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('pmid', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=200), nullable=True),
    sa.Column('abstract', sa.String(length=1000), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
    sa.Column('lastmodified', sa.DateTime(timezone=True), nullable=True),
    sa.Column('deleted', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_articles')
    op.drop_table('recommend_articles')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_last_name'), table_name='users')
    op.drop_index(op.f('ix_users_first_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
