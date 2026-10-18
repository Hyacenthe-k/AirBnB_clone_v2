#!/usr/bin/python3
"""Fabric script that distributes an archive to web servers"""
from fabric.api import env, put, run
import os

env.hosts = ['34.207.10.115', '54.157.32.137'] if not env.hosts else env.hosts
env.user = 'ubuntu'

def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        filename = os.path.basename(archive_path)
        no_ext = filename.replace(".tgz", "")
        remote_tmp = "/tmp/{}".format(filename)
        release_dir = "/data/web_static/releases/{}".format(no_ext)

        # Upload the archive
        put(archive_path, remote_tmp)

        # Uncompress to release folder
        run("mkdir -p {}".format(release_dir))
        run("tar -xzf {} -C {}".format(remote_tmp, release_dir))
        run("rm {}".format(remote_tmp))

        # Move files up and remove empty folder
        run("mv {}/web_static/* {}".format(release_dir, release_dir))
        run("rm -rf {}/web_static".format(release_dir))

        # Update symlink
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_dir))

        print("New version deployed!")
        return True
    except Exception as e:
        print("Deploy failed: {}".format(e))
        return False
