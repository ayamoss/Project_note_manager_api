"""initial tables

Revision ID: 330acf37c686
Revises: 
Create Date: 2026-09-22 23:17:25.405064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '330acf37c686'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('category',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('note',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['category.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('note')
    op.drop_table('category')
