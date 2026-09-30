#!/usr/bin/python3
"""Defines the BaseModel class."""
import uuid
from datetime import datetime
import models

class BaseModel:
    """A base class for all models in the hbnb clone."""

    def __init__(self, *args, **kwargs):
        """Instantiates a new model."""
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """Returns a string representation of the instance."""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format."""
        dictionary = self.__dict__.copy()
        dictionary["__class__"] = self.__class__.__name__
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        return dictionary
