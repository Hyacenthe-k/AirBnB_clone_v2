#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to web servers"""
from fabric.api import env, put, run, local
from datetime import datetime
import os


def do_pack():
    """Generates a .tgz archive from web_static/"""
    try:
        if not os.path.isdir("versions"):
            local("mkdir -p versions")

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


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        filename = os.path.basename(archive_path)
        no_ext = filename.replace(".tgz", "")
        remote_tmp = "/tmp/{}".format(filename)
        release_dir = "/data/web_static/releases/{}".format(no_ext)

        put(archive_path, remote_tmp)
        run("mkdir -p {}".format(release_dir))
        run("tar -xzf {} -C {}".format(remote_tmp, release_dir))
        run("rm {}".format(remote_tmp))
        run("mv {}/web_static/* {}".format(release_dir, release_dir))
        run("rm -rf {}/web_static".format(release_dir))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_dir))

        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """Creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
