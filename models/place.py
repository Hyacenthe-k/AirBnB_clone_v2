#!/usr/bin/python3
"""This module defines a class Place"""
import os
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'),
           primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'),
           primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """This class defines a place by various attributes"""
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship(
            'Review', backref='place',
            cascade='all, delete-orphan'
        )
        amenities = relationship(
            'Amenity', secondary=place_amenity,
            backref='place_amenities', viewonly=False
        )
    else:
        @property
        def reviews(self):
            """Returns the list of Review instances with place_id == self.id"""
            from models import storage
            all_reviews = storage.all('Review').values()
            return [r for r in all_reviews if r.place_id == self.id]

        @property
        def amenities(self):
            """Returns the list of Amenity instances in amenity_ids"""
            from models import storage
            all_am = storage.all('Amenity').values()
            return [a for a in all_am if a.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Appends an Amenity.id to amenity_ids"""
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
