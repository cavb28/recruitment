#!/usr/bin/python3
""" holds class State"""
import models
from models.base_model import BaseModel, Base
from models.victim import Victim
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Representation of state """
    if models.storage_t == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        victims = relationship("Victim", backref="state", cascade="delete")
    else:
        name = ""
        victims = 0

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

