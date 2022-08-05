"""Add comment table 

Revision ID: 47a5bec61d82
Revises: 2424c68a27d0
Create Date: 2022-07-26 14:44:47.605649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47a5bec61d82'
down_revision = '2424c68a27d0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('article_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('ulm', sa.Integer(), nullable=False),
    sa.Column('dlm', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['status'], ['status.code'], ),
    sa.ForeignKeyConstraint(['ulm'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('article', 'status',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key(None, 'user', 'userrole', ['role_id'], ['id'])
    op.create_foreign_key(None, 'user', 'user', ['ulm'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.alter_column('article', 'status',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_table('comment')
    # ### end Alembic commands ###