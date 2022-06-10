import os
import re
from typing import Optional, List

from app.files import models, storage, schemas
from app.database.db import Session

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

bucket = storage.MINIO()


def create(req) -> Optional[models.BaseFile]:
    DBSession = Session()

    file_name = req.POST.get('file').filename
    file = req.POST.get('file').file
    size = os.fstat(file.fileno())
    folder_id = req.POST.get('folder_id')
    file_type = re.split(r"\.", file_name)

    bucket.load_file(file_name, file, size.st_size)

    DBFile = models.BaseFile(file_name=file_name,
                             size=size.st_size,
                             type=file_type[-1],
                             folder_id=folder_id)

    try:
        DBSession.add(DBFile)
        DBSession.commit()
        DBSession.refresh(DBFile)
    except IntegrityError:
        return None

    return DBFile


def read(schema: schemas.NameFilePatch) -> Optional[models.BaseFile]:
    DBSession = Session()

    DBFile = DBSession.execute(select(models.BaseFile).
                               where(models.BaseFile.file_name == schema.file_name)).scalar()

    if not DBFile:
        return None

    return DBFile


def read_all(schema: schemas.FileReadAll) -> List[Optional[models.BaseFile]]:
    DBSession = Session()

    if schema.sort_value:
        files = DBSession.execute(select(models.BaseFile)
                                  .where(models.BaseFile.folder_id == schema.folder_id)
                                  .order_by(schema.sort_value)).scalars().all()

        return files


def download(schema: schemas.IdFilePath):
    DBSession = Session()

    DBFile = DBSession.execute(select(models.BaseFile).
                               where(models.BaseFile.id == schema.files_id)).scalar()

    if not DBFile:
        return None

    file = bucket.download_file(DBFile.file_name)

    return DBFile.file_name, file


def read_for_share(schema_id: schemas.IdFilePath) -> Optional[str]:
    DBSession = Session()

    DBFile = DBSession.execute(select(models.BaseFile).
                               where(models.BaseFile.id == schema_id.files_id)).scalar()

    if not DBFile:
        return None

    link = bucket.share_file_link(DBFile.file_name)

    if not link:
        return None

    return link


def update(schema_id: schemas.IdFilePath, schema: schemas.UpdateFile) -> Optional[models.BaseFile]:
    DBSession = Session()

    DBFile = DBSession.execute(select(models.BaseFile).
                               where(models.BaseFile.id == schema_id.files_id)).scalar()

    if not DBFile:
        return None

    bucket.update_file(schema.file_name, DBFile.file_name, DBFile.size, DBFile.type)

    DBFile.update(schema.file_name, DBFile.type)

    try:
        DBSession.add(DBFile)
        DBSession.commit()
        DBSession.refresh(DBFile)
    except IntegrityError:
        return None

    return DBFile


def move(schema_id: schemas.IdFilePath, schema: schemas.UpdateFile) -> Optional[models.BaseFile]:
    DBSession = Session()

    DBFile = DBSession.execute(select(models.BaseFile).
                               where(models.BaseFile.id == schema_id.files_id)).scalar()

    if not DBFile:
        return None

    DBFile.move(schema.folder_id)

    DBSession.add(DBFile)
    DBSession.commit()
    DBSession.refresh(DBFile)

    return DBFile


def delete(schema_id: schemas.IdFilePath) -> Optional[str]:
    DBSession = Session()

    DBFile = DBSession.execute(select(models.BaseFile).
                               where(models.BaseFile.id == schema_id.files_id)).scalar()

    if not DBFile:
        return None

    bucket.delete_file(DBFile.file_name)

    DBSession.delete(DBFile)
    DBSession.commit()

    return 'success'
