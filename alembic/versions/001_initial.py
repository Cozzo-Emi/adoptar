"""initial tables

Revision ID: 001
Revises:
Create Date: 2026-06-03

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'usuario',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False, unique=True),
        sa.Column('telefono', sa.String(length=20), nullable=True),
        sa.Column('password_hash', sa.Text(), nullable=False),
        sa.Column('rol', sa.Enum('admin', 'adoptante', name='user_role'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.UniqueConstraint('email', name='uq_usuario_email')
    )
    op.create_index('ix_usuario_id', 'usuario', ['id'], unique=False)
    op.create_index('ix_usuario_email', 'usuario', ['email'], unique=True)

    op.create_table(
        'animal',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('especie', sa.String(length=100), nullable=False),
        sa.Column('raza', sa.String(length=100), nullable=True),
        sa.Column('edad', sa.Integer(), nullable=True),
        sa.Column('descripcion', sa.String(length=500), nullable=True),
        sa.Column('imagen', sa.String(length=500), nullable=True),
        sa.Column('estado', sa.Enum('disponible', 'en_proceso', 'adoptado', name='animal_status'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_animal_id', 'animal', ['id'], unique=False)

    op.create_table(
        'solicitud',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('estado', sa.Enum('pendiente', 'aprobada', 'rechazada', name='request_status'), nullable=False),
        sa.Column('id_usuario', sa.Integer(), nullable=False),
        sa.Column('id_animal', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id'], name='fk_solicitud_usuario'),
        sa.ForeignKeyConstraint(['id_animal'], ['animal.id'], name='fk_solicitud_animal'),
        sa.UniqueConstraint('id_usuario', 'id_animal', name='uq_usuario_animal')
    )
    op.create_index('ix_solicitud_id', 'solicitud', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_solicitud_id', table_name='solicitud')
    op.drop_table('solicitud')
    op.drop_index('ix_animal_id', table_name='animal')
    op.drop_table('animal')
    op.drop_index('ix_usuario_email', table_name='usuario')
    op.drop_index('ix_usuario_id', table_name='usuario')
    op.drop_table('usuario')