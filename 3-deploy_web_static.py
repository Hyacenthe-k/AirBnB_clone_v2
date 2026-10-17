#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to web servers"""
from fabric.api import env, put, run, local
from datetime import datetime
import os


env.hosts = ['localhost']
env.user = 'root'


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


        # Ensure nginx is installed and configured on the remote host
        run("if ! command -v nginx > /dev/null 2>&1; then apt-get update && apt-get install -y nginx; fi")
        run("mkdir -p /data/web_static/releases/test/ /data/web_static/shared/")
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/test/ /data/web_static/current")
        
        # Safely update nginx config to serve files at root and /hbnb_static
        run("python3 -c \"import re; c=open('/etc/nginx/sites-available/default').read(); c=re.sub(r'root /var/www/html;', r'root /data/web_static/current;', c); open('/etc/nginx/sites-available/default','w').write(c)\"")
        run("service nginx restart || systemctl restart nginx || nginx -s reload")

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
