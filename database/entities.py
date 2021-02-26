"""Contains all the classes related to tables in the database and its relationships,
declared based on SQLAlchemy ORM."""
from typing import Optional

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

BaseORM = declarative_base()


class Profile(BaseORM):
    """Object representation of "profiles" table."""
    __tablename__ = "profiles"
    __id = Column("profile_id", Integer, primary_key=True)
    name = Column("name", String, unique=True, nullable=False)
    password = Column("password", String, nullable=False)
    # relationships
    formats = relationship("Format", back_populates="profile")

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

    @property
    def id(self):
        """"returns id of the current object, non modifiable"""
        return self.__id


class Password(BaseORM):
    """Object representation of "passwords" table."""
    __tablename__ = "passwords"
    __id = Column("password_id", Integer, primary_key=True)
    password = Column("password", String, nullable=False)
    creation_date = Column("creation_date", Date, nullable=False)
    __status_id = Column("status_id", Integer, ForeignKey("statuses.status_id"), nullable=False)
    __account_id = Column("account_id", Integer, ForeignKey("account.account_id"), nullable=False)
    # relationships
    account = relationship("Account", back_populates="passwords")
    status = relationship("Status", back_populates="passwords")

    def __init__(
            self,
            *,
            password: str
    ):
        """Create a new :class:`Password` instance.

                        all attributes passed to this constructor must be kwargs::

                            password = Password(password="password")

                        :param password: used to log in to the respective service.
                        """
        self.password = password
        self.creation_date = Date()

    @property
    def id(self):
        """"returns id of the current object, non modifiable"""
        return self.__id


class Account(BaseORM):
    """Object representation of "accounts" table."""
    __tablename__ = "accounts"
    __id = Column("account_id", Integer, primary_key=True)
    user = Column("user", String, nullable=False)
    __service_id = Column("service_id", Integer, ForeignKey("services.service_id"), nullable=False)
    # relationships
    service = relationship("Service", back_populates="accounts")
    passwords = relationship("Password", order_by=Password.creation_date, back_populates="account")

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

    @property
    def id(self):
        """"returns id of the current object, non modifiable"""
        return self.__id


class LifespanType(BaseORM):
    """Object representation of "lifespan_types" table."""
    __tablename__ = "lifespan_types"
    __id = Column("lifespan_type_id", Integer, primary_key=True)
    type_ = Column("type", String, unique=True, nullable=False)
    # relationships
    services = relationship("Service", back_populates="lifespan_type")

    @property
    def id(self):
        """"returns id of the current object, non modifiable"""
        return self.__id


class Service(BaseORM):
    """Object representation of "services" table."""
    __tablename__ = "services"
    __id = Column("service_id", Integer, primary_key=True)
    name = Column("name", String, unique=True, nullable=False)
    accepts_duplicates = Column("accepts_duplicates", Integer, nullable=False)
    minimum_length = Column("minimum_length", Integer, nullable=False)
    maximum_length = Column("maximum_length", Integer, nullable=False)
    lifespan_amount = Column("lifespan_amount", Integer, nullable=False)
    __lifespan_type_id = Column("lifespan_type_id", Integer, ForeignKey("lifespan_types.lifespan_type_id"),
                                nullable=False)
    __format_id = Column("format_id", Integer, ForeignKey("formats.format_id"), nullable=False)
    __profile_id = Column("profile_id", Integer, ForeignKey(), nullable=False)
    # relationships
    format = relationship("Format", back_populates="services")
    lifespan_type = relationship("LifespanType", back_populates="services")
    accounts = relationship("Account", back_populates="service")

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

    @property
    def id(self):
        """"returns id of the current object, non modifiable"""
        return self.__id


class Format(BaseORM):
    """Object representation of "formats" table."""
    __tablename__ = "formats"
    __id = Column("format_id", Integer, primary_key=True)
    name = Column("name", String, nullable=False, unique=True)
    regex = Column("regex", String, nullable=False)
    description = Column("description", String, nullable=True)
    # relationships
    profile = relationship("Profile", back_populates="formats")
    services = relationship("Service", back_populates="format")

    def __init__(
            self,
            *,
            name: str,
            regex: str,
            description: Optional[str] = None
    ):
        """Create a new :class:`Format` instance.

                all attributes passed to this constructor must be kwargs::

                    format = Format(name="service_name", regex="pattern")

                :param name: uniquely identifies the format.

                :param regex: patter the format has to follow.

                :param description=None: specifies a description of the format´s behaviour.
                """
        self.name = name
        self.regex = regex
        self.description = description

    @property
    def id(self):
        """"returns id of the current object, non modifiable"""
        return self.__id


class Status(BaseORM):
    """Object representation of "statuses" table."""
    __tablename__ = "statuses"
    __id = Column("status_id", Integer, primary_key=True)
    status = Column("status", String, nullable=False, unique=True)
    # relationships
    passwords = relationship("Password", back_populates="status")

    @property
    def id(self):
        """"returns id of the current object, non modifiable"""
        return self.__id
