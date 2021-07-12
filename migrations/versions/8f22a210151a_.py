"""empty message

Revision ID: 8f22a210151a
Revises: 
Create Date: 2021-07-12 15:40:44.448734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f22a210151a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actor',
    sa.Column('id', sa.Integer().with_variant(sa.Integer(), 'sqlite'), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('gender', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('movie',
    sa.Column('id', sa.Integer().with_variant(sa.Integer(), 'sqlite'), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=True),
    sa.Column('release_date', sa.String(length=180), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )

    # Upgrade commands used to populate initial information
    # Populate Movie table
    op.execute("INSERT INTO movie (title, release_date) VALUES ('The Breakfast Club', '19850215');")
    op.execute("INSERT INTO movie (title, release_date) VALUES ('The Goonies', '19850607');")
    op.execute("INSERT INTO movie (title, release_date) VALUES ('Legend', '19851213');")
    op.execute("INSERT INTO movie (title, release_date) VALUES ('Fright Night', '19850802');")
    op.execute("INSERT INTO movie (title, release_date) VALUES ('Back to the Future', '19850703');")

    # Populate Actor table
    op.execute("INSERT INTO actor (name, age, gender) VALUES ('Molly Ringwald', '53', 'Female');")
    op.execute("INSERT INTO actor (name, age, gender) VALUES ('Sean Astin', '50', 'Male');")
    op.execute("INSERT INTO actor (name, age, gender) VALUES ('Tim Curry', '75', 'Male');")
    op.execute("INSERT INTO actor (name, age, gender) VALUES ('Amanda Bearse', '62', 'Female');")
    op.execute("INSERT INTO actor (name, age, gender) VALUES ('Michael J. Fox', '60', 'Male');")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movie')
    op.drop_table('actor')
    # ### end Alembic commands ###
