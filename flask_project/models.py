from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from typing import List
import logging
from sqlalchemy.orm import Mapped,relationship,sessionmaker
from sqlalchemy import UniqueConstraint,ForeignKey,create_engine

class Base(DeclarativeBase):
  def __repr__(self):
    return f"{self.__class__.__name__}(id={self.id})"

db = SQLAlchemy(model_class=Base)


class Category(Base):
  __tablename__= "category"
  __table_args__ = (UniqueConstraint('name'),)
  id    : Mapped[int] = mapped_column(primary_key=True)
  name  : Mapped[str] = mapped_column(String(50))
  products :Mapped[list["Product"]] = relationship("Product",back_populates="category", cascade="all, delete-orphan")

class Product(Base):
  __tablename__= "product"
  __table_args__ = (UniqueConstraint('name'),)
  id    : Mapped[int] = mapped_column(primary_key=True)
  name  : Mapped[str] = mapped_column(String(50))
  price : Mapped[int] = mapped_column()
  category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
  category:Mapped["Category"] = relationship("Category",back_populates="products")
  images = relationship("Image",back_populates="product", cascade="all, delete-orphan")


class Image(Base):
  __tablename__= "image"
  __table_args__ = (UniqueConstraint('image_url'),)
  id : Mapped[int] = mapped_column(primary_key=True) 
  image_url : Mapped[str] = mapped_column(String(255))
  product_id : Mapped[int] = mapped_column(ForeignKey("product.id"))
  product = relationship("Product",back_populates="images")

def init_db(db_uri='postgresql://postgres:postgres@localhost:5432/flask_db'):
    logger = logging.getLogger("FlaskApp")
    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
    logger.info("Created database")

def get_session(db_uri):
    engine = create_engine(db_uri)
    Session = sessionmaker(bind = engine)
    session = Session()
    return session
  
 