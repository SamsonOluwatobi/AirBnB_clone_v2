#!/usr/bin/python3
""" fabfile that distribute an archive to web servers"""
import os
from datetime import datetime
from fabric.api import *


# host IP addresses for web-01 && web-02
env.hosts = ['100.26.227.3', '100.25.182.54']
env.user = "ubuntu"


def do_pack():
    """ create an a .tgz achive"""
    cur_date_time = datetime.now().strftime("%Y%m%d%H%M%S")

    archive_path = "versions/web_static_{}.tgz".format(cur_date_time)

    local("mkdir -p versions")

    tgz_archive = local("tar -cvzf {} web_static".format(archive_path))

    if tgz_archive.return_code != 0:
        return None
    else:
        return archive_path


def do_deploy(archive_path):
    """Deploy the archive to web servers."""
    if os.path.exists(archive_path):
        file_name = archive_path[9:]

        newest_version_path = "/data/web_static/releases/" + file_name[:-4]

        archive_file_path = "/tmp/" + file_name

        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(newest_version_path))

        run("sudo tar -xzf {} -C {}/"
            .format(archive_file_path, newest_version_path))

        run("sudo rm {}".format(archive_file_path))

        run("sudo mv {}/web_static/* {}"
            .format(newest_version_path, newest_version_path))

        run("sudo rm -rf {}/web_static"
            .format(newest_version_path))

        run("sudo rm -rf /data/web_static/current")

        run("sudo ln -s {} /data/web_static/current"
            .format(newest_version_path))

        print("New version deployed!")
        return True

    return False
