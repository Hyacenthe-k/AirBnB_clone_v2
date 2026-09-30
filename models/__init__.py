#!/usr/bin/python3
"""Initializes the models package with a unique FileStorage instance.

Any module that needs to read or write objects imports the `storage`
variable defined here rather than creating its own FileStorage instance,
guaranteeing a single shared source of truth for the whole application.
"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
