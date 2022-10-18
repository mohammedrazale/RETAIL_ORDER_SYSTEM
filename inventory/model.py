""" Models to support inventory service. """
from sqlalchemy import Column, Integer, String, REAL
from sqlalchemy.ext.declarative import declarative_base
from RETAIL_ORDER_SYSTEM.inventory.db import Session
from RETAIL_ORDER_SYSTEM.inventory.exceptions import NoSuchProductException


Base = declarative_base()


class Product(Base):
    """Products table within the inventory DB."""

    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(REAL, nullable=False)
    stock = Column(Integer, nullable=False)


class InventoryProduct:
    """Represents a product within an inventory."""

    def __init__(self, product_id):
        with Session() as session:
            product = session.query(Product).get(product_id)
            if not product:
                raise NoSuchProductException()
            product.__dict__.pop("_sa_instance_state", None)
            self.__dict__.update(product.__dict__)

    def as_dict(self):
        """Return a dict representaton."""
        return self.__dict__

    def update(self, attribute_dict):
        """Update attributes of product."""
        with Session() as session:
            self.__dict__.update(attribute_dict)
            session.query(Product).filter(Product.id == self.id).update(attribute_dict)
            session.commit()
        return self

    @classmethod
    def create(cls, name, price, stock):
        """Create a new product from attributes."""
        with Session() as session:
            new_prod = Product(name=name, price=price, stock=stock)
            session.add(new_prod)
            session.commit()
            return cls(new_prod.id)

    @classmethod
    def get_all(cls):
        """Get all products in inventory."""
        with Session() as session:
            for product in session.query(Product).all():
                yield cls(product.id)


def create_db(engine):
    """Create the DB and tables"""
    Base.metadata.create_all(engine)
