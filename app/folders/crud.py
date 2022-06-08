import json

from app.folders import models, schemas
from app.database.db import Session

from sqlalchemy.future import select


def create(schema: schemas.CreateFolder):
    DBSession = Session()

    verify_folder = DBSession.execute(select(models.BaseFolder)
                                      .where(models.BaseFolder.folder_name == schema.folder_name))

    if verify_folder.scalar():
        return None

    folder = models.BaseFolder(folder_name=schema.folder_name, user_id=schema.user_id)

    DBSession.add(folder)
    DBSession.commit()
    DBSession.refresh(folder)

    return json.loads(schemas.ReadFolder.from_orm(folder).json())


def read(schema: schemas.IdFolderPath):
    DBSession = Session()

    folder = DBSession.execute(select(models.BaseFolder)
                               .where(models.BaseFolder.id == schema.folder_id)).scalar()

    if not folder:
        return None

    return json.loads(schemas.ReadFolder.from_orm(folder).json())


def read_all():
    DBSession = Session()

    folders = DBSession.execute(select(models.BaseFolder)).scalars().all()

    return [json.loads(schemas.ReadFolder.from_orm(folder).json()) for folder in folders]


def update(schema: schemas.UpdateFolder, schema_id: schemas.IdFolderPath):
    DBSession = Session()

    folder = DBSession.execute(select(models.BaseFolder)
                                      .where(models.BaseFolder.id == schema_id.folder_id)).scalar()

    if not folder:
        return None

    verify_folder = DBSession.execute(select(models.BaseFolder)
                                      .where(models.BaseFolder.folder_name == schema.folder_name))

    if verify_folder.scalar():
        return None

    folder.update(schema.folder_name)

    DBSession.add(folder)
    DBSession.commit()
    DBSession.refresh(folder)

    return json.loads(schemas.ReadFolder.from_orm(folder).json())


def delete(schema: schemas.IdFolderPath):
    DBSession = Session()

    folder = DBSession.execute(select(models.BaseFolder)
                               .where(models.BaseFolder.id == schema.folder_id)).scalar()

    if not folder:
        return None

    DBSession.delete(folder)
    DBSession.commit()

    return 'success'
