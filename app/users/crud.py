from app.database.db import Session

from app.users import models


def create(req) -> models.BaseUser:
    DBSession = Session()

    name = req.POST.get('name')
    password = req.POST.get('password')

    user = models.BaseUser(name=name, password=password)

    DBSession.add(user)
    DBSession.commit()
    DBSession.refresh(user)

    return user
