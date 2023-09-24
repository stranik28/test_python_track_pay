"""initial

Revision ID: 071b5653a6d6
Revises: 
Create Date: 2023-09-23 01:16:59.995243

"""
from alembic import op
import sqlalchemy as sa

revision = '071b5653a6d6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('payment_status',
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('sort', sa.Integer(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_payment_status')),
                    sa.UniqueConstraint('id', name=op.f('uq_payment_status_id')),
                    sa.UniqueConstraint('sort', name=op.f('uq_payment_status_sort'))
                    )
    op.create_table('ride_status',
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('sort', sa.Integer(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_ride_status')),
                    sa.UniqueConstraint('id', name=op.f('uq_ride_status_id')),
                    sa.UniqueConstraint('sort', name=op.f('uq_ride_status_sort'))
                    )
    op.create_table('transport_type',
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_transport_type')),
                    sa.UniqueConstraint('id', name=op.f('uq_transport_type_id'))
                    )
    op.create_table('user',
                    sa.Column('first_name', sa.Text(), nullable=False),
                    sa.Column('last_name', sa.Text(), nullable=False),
                    sa.Column('middle_name', sa.Text(), nullable=False),
                    sa.Column('phone_number', sa.Text(), nullable=True),
                    sa.Column('email', sa.VARCHAR(length=63), nullable=True),
                    sa.Column('active', sa.Boolean(), server_default=sa.text('false'), nullable=True),
                    sa.Column('password', sa.Text(), nullable=False),
                    sa.Column('block', sa.Boolean(), server_default=sa.text('false'), nullable=False),
                    sa.Column('limit_rides', sa.Integer(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
                    sa.UniqueConstraint('email', name=op.f('uq_user_email')),
                    sa.UniqueConstraint('id', name=op.f('uq_user_id')),
                    sa.UniqueConstraint('phone_number', name=op.f('uq_user_phone_number'))
                    )
    op.create_table('sbp_account',
                    sa.Column('account_id', sa.Integer(), nullable=False),
                    sa.Column('active', sa.Boolean(), server_default=sa.text('false'), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_sbp_account_user_id_user'),
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_sbp_account')),
                    sa.UniqueConstraint('id', name=op.f('uq_sbp_account_id'))
                    )
    op.create_index(op.f('ix_sbp_account_account_id'), 'sbp_account', ['account_id'], unique=False)
    op.create_index(op.f('ix_sbp_account_user_id'), 'sbp_account', ['user_id'], unique=False)
    op.create_table('transport',
                    sa.Column('type_id', sa.Integer(), nullable=False),
                    sa.Column('number', sa.VARCHAR(length=6), nullable=False),
                    sa.Column('region_numb', sa.VARCHAR(length=3), nullable=False),
                    sa.Column('price', sa.Integer(), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.Column('route_numb', sa.String, nullable=False),
                    sa.ForeignKeyConstraint(['type_id'], ['transport_type.id'],
                                            name=op.f('fk_transport_type_id_transport_type'), ondelete='RESTRICT'),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_transport')),
                    sa.UniqueConstraint('id', name=op.f('uq_transport_id'))
                    )
    op.create_index(op.f('ix_transport_number'), 'transport', ['number'], unique=True)
    op.create_table('bluetooth_device',
                    sa.Column('transport_id', sa.Integer(), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.ForeignKeyConstraint(['transport_id'], ['transport.id'],
                                            name=op.f('fk_bluetooth_device_transport_id_transport'),
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_bluetooth_device')),
                    sa.UniqueConstraint('id', name=op.f('uq_bluetooth_device_id'))
                    )
    op.create_table('preference_account',
                    sa.Column('account_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.ForeignKeyConstraint(['account_id'], ['sbp_account.id'],
                                            name=op.f('fk_preference_account_account_id_sbp_account'),
                                            ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_preference_account_user_id_user'),
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_preference_account')),
                    sa.UniqueConstraint('account_id', name=op.f('uq_preference_account_account_id')),
                    sa.UniqueConstraint('id', name=op.f('uq_preference_account_id'))
                    )
    op.create_index(op.f('ix_preference_account_user_id'), 'preference_account', ['user_id'], unique=False)
    op.create_table('ride',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('transport_id', sa.Integer(), nullable=False),
                    sa.Column('status_id', sa.Integer(), nullable=False),
                    sa.Column('end_at', sa.TIMESTAMP(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.ForeignKeyConstraint(['status_id'], ['ride_status.id'],
                                            name=op.f('fk_ride_status_id_ride_status'), ondelete='RESTRICT'),
                    sa.ForeignKeyConstraint(['transport_id'], ['transport.id'],
                                            name=op.f('fk_ride_transport_id_transport'), ondelete='RESTRICT'),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_ride_user_id_user'),
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_ride')),
                    sa.UniqueConstraint('id', name=op.f('uq_ride_id'))
                    )
    op.create_table('ride_payment',
                    sa.Column('ride_id', sa.Integer(), nullable=False),
                    sa.Column('account_id', sa.Integer(), nullable=False),
                    sa.Column('amount', sa.Integer(), nullable=False),
                    sa.Column('status_id', sa.Integer(), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.ForeignKeyConstraint(['account_id'], ['sbp_account.id'],
                                            name=op.f('fk_ride_payment_account_id_sbp_account'), ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['ride_id'], ['ride.id'], name=op.f('fk_ride_payment_ride_id_ride'),
                                            ondelete='RESTRICT'),
                    sa.ForeignKeyConstraint(['status_id'], ['payment_status.id'],
                                            name=op.f('fk_ride_payment_status_id_payment_status')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_ride_payment')),
                    sa.UniqueConstraint('id', name=op.f('uq_ride_payment_id'))
                    )
    op.create_table('touches',
                    sa.Column('ride_id', sa.Integer(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('bluetooth_device_id', sa.Integer(), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'),
                              nullable=False),
                    sa.ForeignKeyConstraint(['bluetooth_device_id'], ['bluetooth_device.id'],
                                            name=op.f('fk_touches_bluetooth_device_id_bluetooth_device'),
                                            ondelete='RESTRICT'),
                    sa.ForeignKeyConstraint(['ride_id'], ['ride.id'], name=op.f('fk_touches_ride_id_ride'),
                                            ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_touches_user_id_user'),
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_touches')),
                    sa.UniqueConstraint('id', name=op.f('uq_touches_id'))
                    )
    op.execute('''INSERT INTO transport_type(id, name) VALUES (1, 'Автобус');''')
    op.execute('''INSERT INTO transport(id, type_id, number, region_numb, price, route_numb) VALUES (1, 1,'АБ123В', 123, 40, '12C');''')
    op.execute('''INSERT INTO transport(id, type_id, number, region_numb, price, route_numb) VALUES (2, 1,'АА777А', 93, 40, '4');''')
    op.execute('''INSERT INTO bluetooth_device(id, transport_id) VALUES (1, 1);''')
    op.execute('''INSERT INTO bluetooth_device(id, transport_id) VALUES (2, 2);''')
    op.execute('''INSERT INTO ride_status(id, name, sort) VALUES (1, 'Подтверждена', 1);''')
    op.execute('''INSERT INTO ride_status(id, name, sort) VALUES (2, 'Оплачена', 2);''')
    op.execute('''INSERT INTO payment_status(id, name, sort) VALUES (1, 'Ожидается', 1);''')
    op.execute('''INSERT INTO payment_status(id, name, sort) VALUES (2, 'Оплачено', 2);''')
    op.execute('''INSERT INTO payment_status(id, name, sort) VALUES (3, 'Отклонено', 3);''')
    op.execute(
        '''INSERT INTO public.user(first_name, last_name, middle_name, phone_number, email, active, password, block, 
        limit_rides, id) VALUES ('Александр', 'Бородач', 'Родионович', '+74753149599', 'nikita@trackpay.com', false, 
        '123', false, null, 1);'''
    )
    op.execute('''INSERT INTO sbp_account(user_id, account_id, active) VALUES (1, 1, true);''')


def downgrade():
    op.drop_table('touches')
    op.drop_table('ride_payment')
    op.drop_table('ride')
    op.drop_index(op.f('ix_preference_account_user_id'), table_name='preference_account')
    op.drop_table('preference_account')
    op.drop_table('bluetooth_device')
    op.drop_index(op.f('ix_transport_number'), table_name='transport')
    op.drop_table('transport')
    op.drop_index(op.f('ix_sbp_account_user_id'), table_name='sbp_account')
    op.drop_index(op.f('ix_sbp_account_account_id'), table_name='sbp_account')
    op.drop_table('sbp_account')
    op.drop_table('user')
    op.drop_table('transport_type')
    op.drop_table('ride_status')
    op.drop_table('payment_status')
