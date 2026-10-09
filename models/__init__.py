#!/usr/bin/python3
"""Chooses the storage engine based on HBNB_TYPE_STORAGE"""
import os
import warnings

# Silence MySQL 5.7.8-rc deprecation warning on stderr
# ("@@SESSION.GTID_EXECUTED is deprecated")
warnings.filterwarnings(
    "ignore", message=".*GTID_EXECUTED.*"
)


if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
