#!/usr/bin/python
""" holds class City"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Victim(BaseModel, Base):
    """Representation of city """
    if models.storage_t == "db":
        __tablename__ = 'victims'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        value = Column(Integer, nullable=False)
        #places = relationship("Place", backref="cities", cascade="delete")
    else:
        state_id = ""
        name = 0

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
