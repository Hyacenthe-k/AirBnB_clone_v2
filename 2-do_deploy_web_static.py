#!/usr/bin/python3
"""Fabric script that distributes an archive to web servers"""
import os
from fabric.api import put, run, settings


def do_deploy(archive_path):
    """Distributes an archive to the web servers and deploys it.

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
