import json

from sqlalchemy.future import select

from app.database.db import Session

from app.users import models, schemas


def create(schema: schemas.CreateUser):
    DBSession = Session()

    verify_username = DBSession.execute(select(models.BaseUser)
                                        .where(models.BaseUser.name == schema.name))

    if verify_username.scalar():
        return None

    user = models.BaseUser(name=schema.name, password=schema.password)

    DBSession.add(user)
    DBSession.commit()
    DBSession.refresh(user)

    return json.loads(schemas.ReadUser.from_orm(user).json())



def read(schema: schemas.LoginForm):
    DBSession = Session()

    user = DBSession.execute(select(models.BaseUser).where(models.BaseUser.name == schema.login)).scalar()

    return user
