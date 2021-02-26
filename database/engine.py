from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import database.entities as entities

BASE_STATUSES = (
    "active",
    "expired",
    "changed",
)

BASE_LIFESPAN_TYPES = (
    "day",
    "month",
    "year",
)


def insert_base_lifespan_types(base_data_session):
    """inserts :class:`LifespanType` base values"""
    ls_types = base_data_session.query(entities.LifespanType).all()

    def add_value_if_new(value):
        if value not in (lifespan_type.type_ for lifespan_type in ls_types):
            new_ls = entities.LifespanType()
            new_ls.type_ = value
            base_data_session.add(new_ls)

    for val in BASE_LIFESPAN_TYPES:
        add_value_if_new(val)
    base_data_session.commit()


def insert_base_statuses(base_data_session):
    """inserts :class:`Status` base values"""
    statuses = base_data_session.query(entities.Status).all()

    def add_value_if_new(value):
        if value not in (stat.status for stat in statuses):
            new_status = entities.Status()
            new_status.status = value
            base_data_session.add(new_status)

    for status in BASE_STATUSES:
        add_value_if_new(status)
    base_data_session.commit()


def initialize(__engine):
    """initializes base data on the database as wel as session manager"""
    entities.BaseORM.metadata.create_all(bind=__engine)
    session = sessionmaker(bind=__engine)
    base_data_session = session()
    insert_base_lifespan_types(base_data_session)
    insert_base_statuses(base_data_session)
    return base_data_session


__engine = create_engine("sqlite:///passwords.db")
SESSION = initialize(__engine)

# delete functions to avoid importing them
del initialize
del insert_base_statuses
del insert_base_lifespan_types
del BASE_STATUSES
del BASE_LIFESPAN_TYPES
