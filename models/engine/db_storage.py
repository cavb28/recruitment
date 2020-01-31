#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models

from models.base_model import BaseModel, Base
from models.victim import Victim
from models.state import State
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import jsonify
import json

classes = {"State": State, "Victim": Victim}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}?charset=utf8'
                                      '?charset=utf8'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """method to retrieve one object"""
        if cls and id:
            objs_by_cls = self.all(cls)
            obj_name = "{}.{}".format(cls, id)
            return objs_by_cls.get(obj_name)
        else:
            return None

    def exec(self):
        victms_list = {}
        conn = self.__engine.connect()
        result = conn.execute("CALL GetAllVictims()")
        for element in result:
            dict_tpl = dict(element)
            index = 0
            for k, v in dict_tpl.items():
                if isinstance(v, str):
                    victms_list[k] = v
                else:
                    victms_list[k] = int(v)



            #victms_list.append(dict(element))

        conn.close()
        #jsonify({'result': [dict(row) for row in victms_list]})
        return victms_list

    def count(self, cls=None):
        """method to count the number of objects in storage"""
        return (len(self.all(cls)))

