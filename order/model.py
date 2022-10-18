""" Models to support order service. """
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from RETAIL_ORDER_SYSTEM.order.db import Session
from RETAIL_ORDER_SYSTEM.order.exceptions import NoSuchOrderException


Base = declarative_base()


class _Order(Base):
    """Products table within the inventory DB."""

    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_name = Column(String(255), nullable=False)
    user_ph_no = Column(String(10), nullable=False)
    user_address = Column(String(255), nullable=False)
    product_id = Column(Integer)
    qty = Column(Integer)
    status = Column(String(10))


class Order:
    """Represents a order placed."""

    def __init__(self, order_id):
        with Session() as session:
            order = session.query(_Order).get(order_id)
            if not order:
                raise NoSuchOrderException()
            order.__dict__.pop("_sa_instance_state", None)
            self.__dict__.update(order.__dict__)

    def as_dict(self):
        """Return a dict representaton."""
        return self.__dict__

    def update(self, attribute_dict):
        """Update attributes of order."""
        with Session() as session:
            self.__dict__.update(attribute_dict)
            session.query(_Order).filter(_Order.id == self.id).update(attribute_dict)
            session.commit()
        return self

    def delete(self):
        """Delete attributes of product."""
        with Session() as session:
            session.query(_Order).filter(_Order.id == self.id).delete()
            session.commit()
        return True

    @classmethod
    def create(cls, attributes):
        """Create a new order"""
        with Session() as session:
            new_order = _Order(**attributes)
            session.add(new_order)
            session.commit()
            return cls(new_order.id)

    @classmethod
    def get_all(cls):
        """Get all orders."""
        with Session() as session:
            for order in session.query(_Order).all():
                yield cls(order.id)


def create_db(engine):
    """Create the DB and tables"""
   
    Base.metadata.create_all(engine)
