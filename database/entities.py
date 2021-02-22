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


class Account(BaseORM):
    """Object representation of "accounts" table."""
    __tablename__ = "accounts"
    __id = Column("account_id", Integer, primary_key=True)
    user = Column("user", String, nullable=False)
    __profile_id = Column(Integer, ForeignKey("profiles.profile_id"), nullable=False)
    __service_id = Column(Integer, ForeignKey("services.service_id"), nullable=False)

    def __init__(
            self,
            *,
            user: str
    ):
        """Create a new :class:`Account` instance.

                all attributes passed to this constructor must be kwargs::

                    account = Account(user="username")

                :param user: uniquely identifies this account
                """
        self.user = user
