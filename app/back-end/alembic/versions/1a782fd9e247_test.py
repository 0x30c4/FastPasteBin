"""test

Revision ID: 1a782fd9e247
Revises:
Create Date: 2022-03-19 17:41:57.725047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a782fd9e247'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bindata',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(), nullable=False),
        sa.Column('meta_data', sa.Text(), nullable=True),
        sa.Column('is_tmp', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bindata_id'), 'bindata', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_bindata_id'), table_name='bindata')
    op.drop_table('bindata')
    # ### end Alembic commands ###
