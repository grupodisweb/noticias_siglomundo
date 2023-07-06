"""migracion1.

Revision ID: d6ae83f45e44
Revises: 
Create Date: 2023-07-03 18:11:55.553589

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6ae83f45e44'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Noticias', schema=None) as batch_op:
        batch_op.alter_column('categoria',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=15),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Noticias', schema=None) as batch_op:
        batch_op.alter_column('categoria',
               existing_type=sa.String(length=15),
               type_=sa.VARCHAR(length=30),
               existing_nullable=False)

    # ### end Alembic commands ###