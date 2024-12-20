#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity,
           "City": City,
           "Place": Place,
           "Review": Review,
           "State": State,
           "User": User
           }


class DBStorage:
    """
    manages storage of hbnb models in a database
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        creates the engine self.__engine and session self.__session
        """
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        returns a dictionary of all objects in the database
        """
        new_dict = {}

        if isinstance(cls, str):
            cls = classes.get(cls)

        if cls is not None:
            for obj in self.__session.query(cls):
                key = "{}.{}".format(type(obj).__name__, obj.id)
                new_dict[key] = obj
        else:
            for name, cls in classes.items():
                for obj in self.__session.query(cls):
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """
        creates a new object in the database
        """
        self.__session.add(obj)

    def save(self):
        """
        commits all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        deletes obj from the current database session
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        creates all tables and a new session
        """
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def get(self, cls, id):
        """
        retrieves one object based on class and ID
        """
        if cls in classes.values():
            return self.__session.query(cls).filter_by(id=id).first()
        else:
            return None

    def count(self, cls=None):
        """
        counts the number of objects in storage of a certain class
        """
        if cls is None:
            return sum(self.count(cls) for cls in classes.values())
        if cls in classes.values():
            return self.__session.query(cls).count()
        else:
            return 0

    def close(self):
        """
        closes the current session
        """
        self.__session.remove()
