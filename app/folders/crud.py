from app.folders import models
from app.database.db import Session

from sqlalchemy.future import select


def create(req):
    DBSession = Session()
    folder_name = req.POST.get('folder_name')
    user_id = req.POST.get('user_id')

    verify_folder = DBSession.execute(select(models.BaseFolder).where(models.BaseFolder.folder_name == folder_name))

    if verify_folder.scalar():
        return None

    folder = models.BaseFolder(folder_name=folder_name, user_id=user_id)

    DBSession.add(folder)
    DBSession.commit()
    DBSession.refresh(folder)

    return folder


def read(req):
    DBSession = Session()

    folder_id = req.matchdict['folder_id']

    folder = DBSession.get(models.BaseFolder, folder_id)

    return folder


def read_all():
    DBSession = Session()

    folders = DBSession.execute(select(models.BaseFolder))

    return folders.scalars().all()


def update(req):
    DBSession = Session()

    folder_id = req.matchdict['folder_id']
    DBFolder = DBSession.get(models.BaseFolder, folder_id)

    if not DBFolder:
        return None

    DBFolder.update(req.POST.get('folder_name'))

    DBSession.add(DBFolder)
    DBSession.commit()
    DBSession.refresh(DBFolder)

    return DBFolder


def delete(req):
    DBSession = Session()

    folder_id = req.matchdict['folder_id']

    folder = DBSession.get(models.BaseFolder, folder_id)

    DBSession.delete(folder)
    DBSession.commit()

    return 'success'
