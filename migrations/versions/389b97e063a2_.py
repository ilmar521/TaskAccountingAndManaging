"""empty message

Revision ID: 389b97e063a2
Revises: eb3ff595f2c8
Create Date: 2023-05-11 15:49:55.694041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '389b97e063a2'
down_revision = 'eb3ff595f2c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notes_projects',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('detail', sa.Text(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notes_tasks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('detail', sa.Text(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('attachment_tasks', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attachment_tasks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=250), autoincrement=False, nullable=True))

    op.drop_table('notes_tasks')
    op.drop_table('notes_projects')
    # ### end Alembic commands ###
