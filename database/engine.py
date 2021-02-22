from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import database.entities as entities

__engine = create_engine("sqlite:///passwords.db")
entities.BaseORM.metadata.create_all(bind=__engine)
Session = sessionmaker(bind=__engine)
