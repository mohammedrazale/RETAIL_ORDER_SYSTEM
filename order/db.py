""" DB helper.

Notes:
 - https://stackoverflow.com/questions/12223335/
 - https://stackoverflow.com/questions/36090055/
"""
import os
from sqlalchemy.orm import sessionmaker
import sqlalchemy

db_file = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "orders.db"
)
engine = sqlalchemy.create_engine(
    f"sqlite:///{db_file}", connect_args={"check_same_thread": False}
)
Session = sessionmaker(bind=engine)
