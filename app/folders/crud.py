from typing import Optional, List

from app.folders import models, schemas
from app.database.db import Session

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError


def create(schema: schemas.CreateFolder) -> Optional[models.BaseFolder]:
    DBSession = Session()

    folder = models.BaseFolder(folder_name=schema.folder_name, user_id=schema.user_id)

    try:
        DBSession.add(folder)
        DBSession.commit()
        DBSession.refresh(folder)
    except IntegrityError:
        return None

    return folder


def read(schema: schemas.IdFolderPath) -> Optional[models.BaseFolder]:
    DBSession = Session()

    folder = DBSession.execute(select(models.BaseFolder)
                               .where(models.BaseFolder.id == schema.folder_id)).scalar()

    if not folder:
        return None

    return folder


def read_all() -> List[Optional[models.BaseFolder]]:
    DBSession = Session()

    folders = DBSession.execute(select(models.BaseFolder)).scalars().all()

    return folders


def update(schema: schemas.UpdateFolder, schema_id: schemas.IdFolderPath) -> Optional[models.BaseFolder]:
    DBSession = Session()

    folder = DBSession.execute(select(models.BaseFolder)
                                      .where(models.BaseFolder.id == schema_id.folder_id)).scalar()

    if not folder:
        return None

    folder.update(schema.folder_name)

    try:
        DBSession.add(folder)
        DBSession.commit()
        DBSession.refresh(folder)
    except IntegrityError:
        return None

    return folder


def delete(schema: schemas.IdFolderPath) -> Optional[str]:
    DBSession = Session()

    folder = DBSession.execute(select(models.BaseFolder)
                               .where(models.BaseFolder.id == schema.folder_id)).scalar()

    if not folder:
        return None

    DBSession.delete(folder)
    DBSession.commit()

    return 'success'
