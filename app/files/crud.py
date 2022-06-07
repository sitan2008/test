import os
import re

from app.files import models, storage
from app.database.db import Session

from sqlalchemy.future import select

bucket = storage.MINIO()


def create(req):
    DBSession = Session()

    file_name = req.POST.get('file').filename
    file = req.POST.get('file').file
    size = os.fstat(file.fileno())
    folder_id = req.POST.get('folder_id')
    file_type = re.split(r"\.", file_name)

    verify_file = DBSession.execute(select(models.BaseFile).where(models.BaseFile.file_name == file_name))

    if verify_file.scalar():
        return None

    bucket.load_file(file_name, file, size.st_size)

    DBFile = models.BaseFile(file_name=file_name,
                             size=size.st_size,
                             type=file_type[-1],
                             folder_id=folder_id)

    DBSession.add(DBFile)
    DBSession.commit()
    DBSession.refresh(DBFile)

    return DBFile


def read(req):
    DBSession = Session()

    file_id = req.matchdict['files_id']

    DBFile = DBSession.get(models.BaseFile, file_id)

    file = bucket.download_file(DBFile.file_name)

    if not file:
        return None

    bucket.load_file('test', file, 106090)

    return DBFile.file_name, file


def read_for_share(req):
    DBSession = Session()

    file_id = req.matchdict['files_id']

    DBFile = DBSession.get(models.BaseFile, file_id)

    link = bucket.share_file_link(DBFile.file_name)

    if not link:
        return None

    return link


def update(req):
    DBSession = Session()

    file_id = req.matchdict['files_id']
    new_name = req.POST.get('file_name')

    DBFile = DBSession.get(models.BaseFile, file_id)

    bucket.update_file(new_name, DBFile.file_name, DBFile.size, DBFile.type)

    DBFile.update(new_name, DBFile.type)

    DBSession.add(DBFile)
    DBSession.commit()
    DBSession.refresh(DBFile)

    return DBFile


def move(req):
    DBSession = Session()

    file_id = req.matchdict['files_id']
    new_folder = req.POST.get('folder_id')

    DBFile = DBSession.get(models.BaseFile, file_id)

    if not DBFile:
        return None

    DBFile.move(new_folder)

    DBSession.add(DBFile)
    DBSession.commit()
    DBSession.refresh(DBFile)

    return DBFile


def delete(req):
    DBSession = Session()

    file_id = req.matchdict['files_id']

    DBFile = DBSession.get(models.BaseFile, file_id)

    if not DBFile:
        return None

    bucket.delete_file(DBFile.file_name)

    DBSession.delete(DBFile)
    DBSession.commit()

    return 'success'