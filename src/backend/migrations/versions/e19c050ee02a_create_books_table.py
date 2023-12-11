"""create books table

Revision ID: e19c050ee02a
Revises:
Create Date: 2023-12-08 15:39:21.187330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e19c050ee02a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "books",
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=128), nullable=False),
        sa.Column('authors', sa.String(length=256), nullable=False),
        sa.Column('summary', sa.String(length=512), nullable=False),
        sa.Column('publication_year', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=False),
    )
    op.create_unique_constraint('uk_books_title_authors', 'books', ['title', 'authors'])
    op.execute(
        """
            ALTER TABLE
                books
            ADD COLUMN
                ts tsvector GENERATED ALWAYS AS (to_tsvector('english', title || ' ' || authors || ' ' || summary || ' ' || cast(publication_year as varchar))) STORED
        """
    )
    op.execute(
        """
            CREATE INDEX gin_ts ON books USING GIN (ts)
        """
    )

def downgrade() -> None:
    op.drop_table('books')
