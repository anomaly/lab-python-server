"""drops required timestamp value

Revision ID: bcc325226a11
Revises: 80836641fabc
Create Date: 2023-05-07 01:59:33.047306

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bcc325226a11'
down_revision = '80836641fabc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('s3_file_metadata', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('user', 'verification_token_expiry',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('user', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('user', 'verification_token_expiry',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('s3_file_metadata', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    # ### end Alembic commands ###
