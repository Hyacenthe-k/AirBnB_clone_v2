#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to web servers"""
import os
from datetime import datetime
from fabric.api import local, put, run, settings


def do_pack():
    """Generates a .tgz archive from the contents of web_static/

    Returns the archive path on success, None on failure.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)

    with settings(warn_only=True):
        local("mkdir -p versions")
        print("Packing web_static to {}".format(archive_path))
        result = local("tar -cvzf {} web_static".format(archive_path))
    if result.failed or not os.path.isfile(archive_path):
        return None

    size = os.path.getsize(archive_path)
    print("web_static packed: {} -> {}Bytes".format(archive_path, size))
    return archive_path


def do_deploy(archive_path):
    """Distributes an archive to the web servers.

    Returns True on success, False otherwise.
    """
    if not os.path.isfile(archive_path):
        return False

    filename = os.path.basename(archive_path)
    name = os.path.splitext(filename)[0]
    tmp = "/tmp/{}".format(filename)
    release = "/data/web_static/releases/{}".format(name)
    current = "/data/web_static/current"

    with settings(warn_only=True):
        if put(archive_path, tmp).failed:
            return False
        commands = [
            "mkdir -p {}".format(release),
            "tar -xzf {} -C {}".format(tmp, release),
            "rm -f {}".format(tmp),
            "cp -a {}/web_static/. {}/".format(release, release),
            "rm -rf {}/web_static".format(release),
            "rm -rf {}".format(current),
            "ln -s {} {}".format(release, current),
        ]
        for cmd in commands:
            if run(cmd).failed:
                return False

    print("New version deployed!")
    return True


def deploy():
    """Creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
