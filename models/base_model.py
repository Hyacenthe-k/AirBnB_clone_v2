#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models

Base = declarative_base()


def _to_datetime(value):
    """Parses an isoformat string back into a datetime"""
    try:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at
        for key, value in kwargs.items():
            if key == '__class__':
                continue
            if key in ('created_at', 'updated_at') and isinstance(value, str):
                value = _to_datetime(value)
            setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        attrs = dict(self.__dict__)
        attrs.pop('_sa_instance_state', None)
        return '[{}] ({}) {}'.format(type(self).__name__, self.id, attrs)

    def save(self):
        """Updates updated_at and saves the instance to storage"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Converts the instance into a dictionary"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary['__class__'] = type(self).__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary.pop('_sa_instance_state', None)
        return dictionary

    def delete(self):
        """Deletes the current instance from storage"""
        models.storage.delete(self)
