"""Contains all the classes related to tables in the database and its relationships,
declared based on SQLAlchemy ORM."""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

BaseORM = declarative_base()


class Profile(BaseORM):
    """Object representation of "profiles" table."""
    __tablename__ = "profiles"
    __id = Column("profile_id", Integer, primary_key=True)
    name = Column("name", String, unique=True, nullable=False)
    password = Column("password", String, nullable=False)

    def __init__(
            self,
            *,
            name: str,
            password: str
    ):
        """Create a new :class:`Profile` instance.

        all attributes passed to this constructor must be kwargs::

            profile = Profile(name="name", password="password")

        :param name: uniquely identifies the profile.

        :param password: password string (preferably hashed beforehand) to protect
            account access.
        """
        self.name = name
        self.password = password



