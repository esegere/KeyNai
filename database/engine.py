from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import entities

engine = create_engine("sqlite:///passwords.db")
entities.BaseORM.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
