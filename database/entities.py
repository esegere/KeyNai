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

                :param user: uniquely identifies this account.
                """
        self.user = user


class LifespanType(BaseORM):
    """Object representation of "lifespan_types" table."""
    __tablename__ = "lifespan_types"
    __id = Column("lifespan_type_id", Integer, primary_key=True)
    type_ = Column("type", String, unique=True, nullable=False)


class Service(BaseORM):
    """Object representation of "services" table."""
    __tablename__ = "services"
    __id = Column("service_id", Integer, primary_key=True)
    name = Column("name", String, unique=True, nullable=False)
    accepts_duplicates = Column("accepts_duplicates", Integer, nullable=False)
    minimum_length = Column("minimum_length", Integer, nullable=False)
    maximum_length = Column("maximum_length", Integer, nullable=False)
    lifespan_amount = Column("lifespan_amount", Integer, nullable=False)
    lifespan_type = Column(Integer, ForeignKey("lifespan_types.lifespan_type_id"), nullable=False)

    def __init__(
            self,
            *,
            name: str,
            accepts_duplicates: bool = True,
            minimum_length: int = 16,
            maximum_length: int = 16,
            lifespan_amount: int = -1,
    ):
        """Create a new :class:`Service` instance.

                all attributes passed to this constructor must be kwargs::

                    service = Service(name="service_name")

                :param name: uniquely identifies the profile.

                :param accepts_duplicates=True: indicates if the given service
                accepts duplicate versions of the password.

                :param minimum_length=16: minimum length for all the passwords belonging to this service

                :param maximum_length=16: maximum length for all the passwords belonging to this service

                :param lifespan_amount=-1: amount of time all passwords for this service stay active, default -1 means
                undefined; lifespan could be of type days, months or years, given by :class:`LifespanType` values
                """
        self.name = name
        self.accepts_duplicates = accepts_duplicates
        self.minimum_length = minimum_length
        self.maximum_length = maximum_length
        self.lifespan_amount = lifespan_amount
