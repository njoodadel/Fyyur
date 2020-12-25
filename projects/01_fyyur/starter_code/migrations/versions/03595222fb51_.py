"""empty message

Revision ID: 03595222fb51
Revises: 60a16bfbb22e
Create Date: 2020-12-24 20:32:00.701318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03595222fb51'
down_revision = '60a16bfbb22e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_venue', sa.String(), nullable=True))
    op.drop_column('Artist', 'seeking_talent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_talent', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('Artist', 'seeking_venue')
    # ### end Alembic commands ###