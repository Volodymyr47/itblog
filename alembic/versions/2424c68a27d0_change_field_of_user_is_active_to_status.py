"""Change field of User: is_active to status 

Revision ID: 2424c68a27d0
Revises: 115f1aecec18
Create Date: 2022-07-12 14:18:27.653063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2424c68a27d0'
down_revision = '115f1aecec18'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('article', 'status',
               existing_type=sa.INTEGER())


    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userrole', sa.Column('is_active', sa.BOOLEAN(), nullable=True))
    op.drop_constraint(None, 'userrole', type_='foreignkey')
    op.drop_column('userrole', 'status')
    op.add_column('user', sa.Column('is_active', sa.BOOLEAN(), nullable=True))
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'status')
    op.drop_constraint(None, 'article', type_='foreignkey')
    op.alter_column('article', 'status',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_table('sqlite_stat1',
    sa.Column('tbl', sa.NullType(), nullable=True),
    sa.Column('idx', sa.NullType(), nullable=True),
    sa.Column('stat', sa.NullType(), nullable=True)
    )
    op.create_table('sqlite_stat4',
    sa.Column('tbl', sa.NullType(), nullable=True),
    sa.Column('idx', sa.NullType(), nullable=True),
    sa.Column('neq', sa.NullType(), nullable=True),
    sa.Column('nlt', sa.NullType(), nullable=True),
    sa.Column('ndlt', sa.NullType(), nullable=True),
    sa.Column('sample', sa.NullType(), nullable=True)
    )
    # ### end Alembic commands ###
