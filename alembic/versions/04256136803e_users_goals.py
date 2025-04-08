"""users goals

Revision ID: 04256136803e
Revises: 4bb249c04124
Create Date: 2025-04-08 16:57:09.782099

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "04256136803e"
down_revision: Union[str, None] = "4bb249c04124"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_goals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("calories_goal", sa.Integer(), nullable=False),
        sa.Column("water_goal", sa.Float(), nullable=False),
        sa.Column("sleep_goal", sa.Float(), nullable=False),
        sa.Column("steps_goal", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_telegram_id"], ["users.telegram_id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_telegram_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_goals")
    # ### end Alembic commands ###
