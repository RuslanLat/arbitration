"""add models

Revision ID: 3f97bd295ac4
Revises: 
Create Date: 2024-04-13 14:15:19.028061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f97bd295ac4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('docs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time_create', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('filename', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('label', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('filename')
    )
    op.create_index(op.f('ix_docs_time_create'), 'docs', ['time_create'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_docs_time_create'), table_name='docs')
    op.drop_table('docs')
    # ### end Alembic commands ###
