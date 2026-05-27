"""create all tables

Revision ID: 4837b8cce149
Revises:
Create Date: 2026-05-27 22:10:26.514695
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import JSON

revision: str = '4837b8cce149'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(50), unique=True, nullable=False, index=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('display_name', sa.String(50), nullable=False),
        sa.Column('role', sa.String(20), server_default='reviewer'),
        sa.Column('department', sa.String(100), server_default=''),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # contracts
    op.create_table(
        'contracts',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), nullable=False, index=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('contract_type', sa.String(50), server_default=''),
        sa.Column('file_name', sa.String(255), nullable=False),
        sa.Column('file_path', sa.String(500), nullable=False),
        sa.Column('file_size', sa.Integer(), server_default='0'),
        sa.Column('file_type', sa.String(20), nullable=False),
        sa.Column('status', sa.String(20), server_default='pending'),
        sa.Column('raw_text', sa.Text(), server_default=''),
        sa.Column('compliance_score', sa.Integer(), nullable=True),
        sa.Column('risk_level', sa.String(20), nullable=True),
        sa.Column('conclusion', sa.Text(), server_default=''),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('reviewed_at', sa.DateTime(), nullable=True),
    )

    # risk_items
    op.create_table(
        'risk_items',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('contract_id', sa.Integer(), nullable=False, index=True),
        sa.Column('clause_index', sa.Integer(), server_default='0'),
        sa.Column('clause_text', sa.Text(), server_default=''),
        sa.Column('risk_level', sa.String(20), nullable=False),
        sa.Column('category', sa.String(50), server_default=''),
        sa.Column('description', sa.Text(), server_default=''),
        sa.Column('legal_basis', sa.Text(), server_default=''),
        sa.Column('suggestion', sa.Text(), server_default=''),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # review_reports
    op.create_table(
        'review_reports',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('contract_id', sa.Integer(), nullable=False, index=True, unique=True),
        sa.Column('report_data', JSON(), server_default='{}'),
        sa.Column('report_number', sa.String(50), server_default=''),
        sa.Column('generated_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # chat_messages
    op.create_table(
        'chat_messages',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('contract_id', sa.Integer(), nullable=False, index=True),
        sa.Column('role', sa.String(10), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # contract_templates
    op.create_table(
        'contract_templates',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('type', sa.String(50), server_default=''),
        sa.Column('description', sa.Text(), server_default=''),
        sa.Column('file_path', sa.String(500), server_default=''),
        sa.Column('download_count', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('contract_templates')
    op.drop_table('chat_messages')
    op.drop_table('review_reports')
    op.drop_table('risk_items')
    op.drop_table('contracts')
    op.drop_table('users')
