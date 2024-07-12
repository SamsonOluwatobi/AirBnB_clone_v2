#!/usr/bin/python3
""" generates a .tgz archive from the contents of the web_static folder"""
from datetime import datetime
from fabric.api import local


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
