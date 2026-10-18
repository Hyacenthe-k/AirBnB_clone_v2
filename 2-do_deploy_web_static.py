#!/usr/bin/python3
"""Fabric script that distributes an archive to web servers"""
from fabric.api import env, put, run
import os


env.user = 'root'


def do_deploy(archive_path):
    """Distributes an archive to the web servers.

    Returns True if all operations succeeded, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Get the archive filename with and without extension
        filename = os.path.basename(archive_path)
        no_ext = filename.replace(".tgz", "")

        remote_tmp = "/tmp/{}".format(filename)
        release_dir = "/data/web_static/releases/{}".format(no_ext)

        # Upload the archive to /tmp/ on the server
        put(archive_path, remote_tmp)

        # Create the release directory
        run("mkdir -p {}".format(release_dir))

        # Uncompress the archive into the release directory
        run("tar -xzf {} -C {}".format(remote_tmp, release_dir))

        # Delete the archive from the server
        run("rm {}".format(remote_tmp))

        # Move contents out of the nested web_static/ folder
        run("mv {}/web_static/* {}".format(release_dir, release_dir))

        # Remove the now-empty nested folder
        run("rm -rf {}/web_static".format(release_dir))

        # Delete the old symlink
        run("rm -rf /data/web_static/current")

        # Create the new symlink
        run("ln -s {} /data/web_static/current".format(release_dir))

        print("New version deployed!")
        return True
    except Exception:
        return False
