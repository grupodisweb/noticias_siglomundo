"""before updating

Revision ID: 1e1c6c30b4a9
Revises: ce5b6182db97
Create Date: 2023-08-08 17:35:04.309986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e1c6c30b4a9'
down_revision = 'ce5b6182db97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Categorías', schema=None) as batch_op:
        batch_op.alter_column('nombre_interno',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=20),
               existing_nullable=True)
        batch_op.alter_column('nombre_impreso',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=20),
               existing_nullable=True)

    with op.batch_alter_table('Noticias', schema=None) as batch_op:
        batch_op.alter_column('imagen',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=500),
               existing_nullable=False)

    with op.batch_alter_table('Usuarios', schema=None) as batch_op:
        batch_op.alter_column('nombre_usuario',
               existing_type=sa.VARCHAR(length=60),
               nullable=True)
        batch_op.alter_column('codigo',
               existing_type=sa.VARCHAR(length=60),
               type_=sa.String(length=128),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
        batch_op.create_unique_constraint(None, ['nombre_usuario'])
        batch_op.create_unique_constraint(None, ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Usuarios', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
        batch_op.alter_column('codigo',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=60),
               existing_nullable=False)
        batch_op.alter_column('nombre_usuario',
               existing_type=sa.VARCHAR(length=60),
               nullable=False)

    with op.batch_alter_table('Noticias', schema=None) as batch_op:
        batch_op.alter_column('imagen',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)

    with op.batch_alter_table('Categorías', schema=None) as batch_op:
        batch_op.alter_column('nombre_impreso',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)
        batch_op.alter_column('nombre_interno',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)

    # ### end Alembic commands ###
