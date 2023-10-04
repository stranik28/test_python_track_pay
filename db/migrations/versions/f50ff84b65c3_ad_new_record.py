"""Ad new record

Revision ID: f50ff84b65c3
Revises: 2d7437601047
Create Date: 2023-10-04 13:39:55.949285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f50ff84b65c3'
down_revision = '2d7437601047'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('''INSERT INTO bluetooth_device(id, transport_id, mac_address) VALUES (5, 2, '30:AE:A4:74:A2:C6');''')


def downgrade():
    pass