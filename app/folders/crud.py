import json

from app.folders import models, schemas
from app.database.db import Session

from sqlalchemy.future import select


def create(req):
    DBSession = Session()
    schema = schemas.CreateFolder(**req.POST)

    verify_folder = DBSession.execute(select(models.BaseFolder)
                                      .where(models.BaseFolder.folder_name == schema.folder_name))

    if verify_folder.scalar():
        return None

    folder = models.BaseFolder(folder_name=schema.folder_name, user_id=schema.user_id)

    DBSession.add(folder)
    DBSession.commit()
    DBSession.refresh(folder)

    schema = schemas.ReadFolder.from_orm(folder)

    return json.loads(schema.json())


def read(req):
    DBSession = Session()

    folder_id = req.matchdict['folder_id']

    folder = DBSession.get(models.BaseFolder, folder_id)

    if not folder:
        return None

    schema = schemas.ReadFolder.from_orm(folder)

    return json.loads(schema.json())


def read_all():
    DBSession = Session()

    folders = DBSession.execute(select(models.BaseFolder)).scalars().all()

    return [json.loads(schemas.ReadFolder.from_orm(folder).json()) for folder in folders]


def update(req):
    DBSession = Session()

    folder_id = req.matchdict['folder_id']
    schema = schemas.UpdateFolder(**req.POST)
    folder = DBSession.get(models.BaseFolder, folder_id)

    if not folder:
        return None

    verify_folder = DBSession.execute(select(models.BaseFolder)
                                      .where(models.BaseFolder.folder_name == schema.folder_name))

    if verify_folder.scalar():
        return None

    folder.update(req.POST.get(schema.folder_name))

    DBSession.add(folder)
    DBSession.commit()
    DBSession.refresh(folder)

    schema = schemas.ReadFolder.from_orm(folder)

    return json.loads(schema.json())


def delete(req):
    DBSession = Session()

    folder_id = req.matchdict['folder_id']

    folder = DBSession.get(models.BaseFolder, folder_id)

    DBSession.delete(folder)
    DBSession.commit()

    return 'success'
