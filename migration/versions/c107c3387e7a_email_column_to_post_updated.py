"""email column to post_updated

Revision ID: c107c3387e7a
Revises: 9f60e961e9d5
Create Date: 2022-12-29 15:12:23.110101

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'c107c3387e7a'
down_revision = '9f60e961e9d5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('creator_email', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.drop_column('posts', 'email')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('posts', 'creator_email')
    # ### end Alembic commands ###