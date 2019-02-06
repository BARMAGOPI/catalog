#!/user/bin/env python3

import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    __tablename__ = 'product'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


@property
def serialize(self):
    # Returns object data in easily serializable format
    return {
        'name': self.name,
        'id': self.id,
        }


class MenuItem(Base):

    __tablename__ = 'menuitems'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    img = Column(String(100))
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


@property
def serialize(self):
    # Returns object data in easily serializable format
    return {
        'name': self.name,
        'description': self.description,
        'course': self.course,
        'price': self.price,
        'id': self.id,

        }
engine = create_engine('sqlite:///products.db')

Base.metadata.create_all(engine)
