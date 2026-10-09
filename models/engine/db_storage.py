#!/usr/bin/python3
"""This module defines a DBStorage class using SQLAlchemy"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity


classes = {
    'User': User, 'State': State, 'City': City,
    'Place': Place, 'Review': Review, 'Amenity': Amenity,
}


class DBStorage:
    """Interacts with a MySQL database via SQLAlchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine and drops tables if HBNB_ENV=test"""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db),
            pool_pre_ping=True
        )
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Returns a dict of objects, filtered by class if given"""
        self.__ensure_tables()
        result = {}
        if cls is None:
            for klass in classes.values():
                for obj in self.__session.query(klass).all():
                    key = '{}.{}'.format(type(obj).__name__, obj.id)
                    result[key] = obj
        else:
            if isinstance(cls, str):
                cls = classes.get(cls)
            for obj in self.__session.query(cls).all():
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                result[key] = obj
        return result

    def new(self, obj):
        """Adds obj to the current session"""
        self.__ensure_tables()
        self.__session.add(obj)

    def save(self):
        """Commits the current session"""
        self.__ensure_tables()
        try:
            self.__session.commit()
        except Exception:
            self.__session.rollback()
            raise

    def rollback(self):
        """Rolls back the current session"""
        self.__session.rollback()

    def delete(self, obj=None):
        """Deletes obj from the current session if not None"""
        if obj is not None:
            self.__ensure_tables()
            self.__session.delete(obj)

    def reload(self):
        """Creates the session; defers create_all if the DB is unreachable"""
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)
        self.__tables_created = False
        self.__try_create_tables()

    def __try_create_tables(self):
        """Runs Base.metadata.create_all once, tolerating failures"""
        if self.__tables_created:
            return True
        try:
            Base.metadata.create_all(self.__engine)
            self.__tables_created = True
            return True
        except Exception:
            return False

    def __ensure_tables(self):
        """Retries create_all lazily before any DB operation"""
        if not self.__tables_created:
            self.__try_create_tables()
