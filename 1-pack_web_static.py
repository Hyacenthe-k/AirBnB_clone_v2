#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from web_static"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Generates a .tgz archive from the contents of web_static/
    Returns the archive path on success, None on failure.
    """
    try:
        # Create versions/ if it doesn't exist
        if not os.path.isdir("versions"):
            local("mkdir -p versions")

        # Build timestamped filename: web_static_YYYYMMDDHHMMSS.tgz
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)

        print("Packing web_static to {}".format(archive_path))
        local("tar -cvzf {} web_static".format(archive_path))

        size = os.path.getsize(archive_path)
        print("web_static packed: {} -> {}Bytes".format(archive_path, size))

        return archive_path
    except Exception:
        return None
