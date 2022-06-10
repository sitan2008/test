import json

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.database.db import Session

from app.users import models, schemas


def create(schema: schemas.CreateUser):
    DBSession = Session()

    user = models.BaseUser(username=schema.username, password=schema.password)

    try:
        DBSession.add(user)
        DBSession.commit()
        DBSession.refresh(user)
    except IntegrityError:
        return None

    return json.loads(schemas.ReadUser.from_orm(user).json())



def read(schema: schemas.LoginForm):
    DBSession = Session()

    user = DBSession.execute(select(models.BaseUser).where(models.BaseUser.username == schema.username)).scalar()

    return user
