#!/usr/bin/env python
#
# Quick postgres read test based on https://docs.sqlalchemy.org/en/14/orm/quickstart.html
#
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

#### Define metadata for our tables

Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )
    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
    user = relationship("User", back_populates="addresses")
    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

# Set authentication parameters

user = 'postgres'

password = 'mysecretpassword'

# Define connection engine

from sqlalchemy import create_engine

engine = create_engine(f"postgresql://{user}:{password}@localhost/postgres", echo=True, future=True)

# Read test data from database

from sqlalchemy.orm import Session
from sqlalchemy import select

session = Session(engine)

stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))

for user in session.scalars(stmt):
    print(user)
