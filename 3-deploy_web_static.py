#!/usr/bin/python3
"""Fabric script to create and distribute an archive to web servers"""
import os
from fabric.api import env, local, put, run
from datetime import datetime


env.user = "ubuntu"
env.hosts = ['54.144.139.197', '34.203.29.50']


def do_pack():
    """Create a .tgz archive of the web_static directory"""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    file_path = "versions/web_static_{}.tgz".format(timestamp)
    local("mkdir -p versions")
    result = local("tar -cvzf {} web_static".format(file_path))
    if result.failed:
        return None
    return file_path


def do_deploy(archive_path):
    """Distribute the archive to the web servers"""
    if not os.path.exists(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    file_no_ext = file_name.split('.')[0]
    remote_path = "/data/web_static/releases/{}/".format(file_no_ext)

    try:
        put(archive_path, '/tmp/')

        run('mkdir -p {}'.format(remote_path))

        run('tar -xzf /tmp/{} -C {}'.format(file_name, remote_path))

        run('rm /tmp/{}'.format(file_name))

        run('mv {}web_static/* {}'.format(remote_path, remote_path))

        run('rm -rf /data/web_static/current')

        run('ln -s {} /data/web_static/current'.format(remote_path))
        print("New version deployed!")
        return True

    except Exception as e:
        return False


def deploy():
    """Create and distribute an archive to web servers.

    """
    # Call do_pack() to create the archive
    archive_path = do_pack()

    # Return False if no archive is created
    if archive_path is None:
        return False
    return do_deploy(archive_path)
