import json

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.config import Configurator
from pyramid import httpexceptions
from pyramid.request import Request
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import remember

from wsgiref.simple_server import make_server

from app.folders import crud as folders_crud, schemas as folders_schemas
from app.users import crud as user_crud, schemas as users_schemas
from app.files import crud as files_crud, storage, schemas as files_schema
from app.database import db

bucket = storage.MINIO()


@view_config(route_name='folders_new', renderer='json', request_method='POST')
def folder_create(req: Request):
    try:
        schema = folders_schemas.CreateFolder(**req.POST)
    except:
        return httpexceptions.HTTPBadRequest()
    folder = folders_crud.create(schema)
    if not folder:
        return httpexceptions.HTTPConflict()
    return json.loads(folders_schemas.ReadFolder.from_orm(folder).json())


@view_config(route_name='folders', renderer='json', request_method='GET')
def folder_read(req: Request):
    try:
        folder_id = folders_schemas.IdFolderPath(**req.matchdict)
    except:
        return httpexceptions.HTTPBadRequest()
    folder = folders_crud.read(folder_id)
    if not folder:
        return httpexceptions.HTTPNotFound()
    return json.loads(folders_schemas.ReadFolder.from_orm(folder).json())


@view_config(route_name='folders_all', renderer='json', request_method='GET')
def folder_read_all(req: Request):
    folders = folders_crud.read_all()
    return [json.loads(folders_schemas.ReadFolder.from_orm(folder).json()) for folder in folders]


@view_config(route_name='folders', renderer='json', request_method='PUT')
def folder_update(req: Request):
    try:
        folder_id = folders_schemas.IdFolderPath(**req.matchdict)
        schema = folders_schemas.UpdateFolder(**req.POST)
    except:
        return httpexceptions.HTTPBadRequest()
    folder = folders_crud.update(schema, folder_id)
    if not folder:
        return httpexceptions.HTTPNotFound()
    return json.loads(folders_schemas.ReadFolder.from_orm(folder).json())


@view_config(route_name='folders', renderer='json', request_method='DELETE')
def folder_delete(req: Request):
    try:
        folder_id = folders_schemas.IdFolderPath(**req.matchdict)
    except:
        return httpexceptions.HTTPBadRequest()
    folder = folders_crud.delete(folder_id)
    if not folder:
        return httpexceptions.HTTPNotFound()
    return folder


@view_config(route_name='files_new', renderer='json', request_method='POST')
def file_upload(req: Request):
    file = files_crud.create(req)
    if not file:
        return httpexceptions.HTTPConflict()
    return json.loads(files_schema.ReadFile.from_orm(file).json())


@view_config(route_name='file', renderer='json', request_method='GET')
def file_read(req: Request):
    try:
        file_name = files_schema.NameFilePatch(**req.matchdict)
    except:
        return httpexceptions.HTTPBadRequest()
    file = files_crud.read(file_name)
    if not file:
        return httpexceptions.HTTPNotFound()
    return json.loads(files_schema.ReadFile.from_orm(file).json())


@view_config(route_name='files_all', renderer='json', request_method='PATCH')
def file_read_all(req: Request):
    try:
        schema = files_schema.FileReadAll(**req.POST)
    except:
        return httpexceptions.HTTPBadRequest()
    files = files_crud.read_all(schema)
    return [json.loads(files_schema.ReadFile.from_orm(file).json()) for file in files]


@view_config(route_name='files', request_method='GET')
def file_download(req: Request):
    try:
        file_id = files_schema.IdFilePath(**req.matchdict)
    except:
        return httpexceptions.HTTPBadRequest()
    file_name, file = files_crud.download(file_id)
    if not file_name:
        return httpexceptions.HTTPNotFound()
    res = Response(body=file.data)
    res.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name
    return res


@view_config(route_name='files', renderer='json', request_method='PUT')
def file_update(req: Request):
    try:
        file_id = files_schema.IdFilePath(**req.matchdict)
        schema = files_schema.UpdateFile(**req.POST)
    except:
        return httpexceptions.HTTPBadRequest()
    if schema.folder_id:
        file = files_crud.move(file_id, schema)
        if not file:
            return httpexceptions.HTTPNotFound()
        return json.loads(files_schema.ReadFile.from_orm(file).json())
    if schema.file_name:
        file = files_crud.update(file_id, schema)
        if not file:
            return httpexceptions.HTTPNotFound()
        return json.loads(files_schema.ReadFile.from_orm(file).json())


@view_config(route_name='files', renderer='json', request_method='DELETE')
def file_delete(req: Request):
    try:
        file_id = files_schema.IdFilePath(**req.matchdict)
    except:
        return httpexceptions.HTTPBadRequest()
    file = files_crud.delete(file_id)
    if not file:
        return httpexceptions.HTTPNotFound()
    return file


@view_config(route_name='files_share', renderer='string', request_method='GET')
def file_share_link(req: Request):
    try:
        file_id = files_schema.IdFilePath(**req.matchdict)
    except:
        return httpexceptions.HTTPBadRequest()
    link = files_crud.read_for_share(file_id)
    if not link:
        return httpexceptions.HTTPNotFound()
    return link


@view_config(route_name='register', renderer='json', request_method='POST')
def registry(req: Request):
    try:
        schema = users_schemas.CreateUser(**req.POST)
    except:
        return httpexceptions.HTTPBadRequest()
    user = user_crud.create(schema)
    if not user:
        return httpexceptions.HTTPConflict()
    return user


@view_config(route_name='auth', renderer='string', request_method='POST')
def login(req: Request):
    try:
        schema = users_schemas.LoginForm(**req.POST)
    except:
        return httpexceptions.HTTPBadRequest()
    user = user_crud.read(schema)
    if user and user.verify_password(schema.password, user.password):
        headers = remember(req, user.id)
        return httpexceptions.HTTPFound(location=req.route_url('folders_all'), headers=headers)
    return httpexceptions.HTTPForbidden()


if __name__ == '__main__':
    db.Base.metadata.create_all()
    bucket.init_bucket()

    settings = {
        'debug_all': True,
        'reload_all': True
    }

    authentication_policy = AuthTktAuthenticationPolicy('secret')

    config = Configurator(settings=settings,
                          authentication_policy=authentication_policy)

    config.include('pyramid_debugtoolbar')
    config.add_route('folders', '/folders/{folder_id}')
    config.add_route('folders_new', '/folders_new')
    config.add_route('folders_all', '/folders_all')
    config.add_route('register', '/register')
    config.add_route('auth', '/auth')
    config.add_route('files_new', '/files_new')
    config.add_route('files', '/files/{files_id}')
    config.add_route('file', '/file/{file_name}')
    config.add_route('files_share', '/files_share/{files_id}')
    config.add_route('files_all', '/files_all')
    config.scan()

    app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
