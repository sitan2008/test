from pyramid.config import Configurator
from pyramid import httpexceptions
from pyramid.request import Request
from pyramid.view import view_config
from pyramid.response import Response

from wsgiref.simple_server import make_server

from app.folders import crud as folders_crud
from app.users import crud as user_crud
from app.files import crud as files_crud, storage
from app.database import db

bucket = storage.MINIO()


@view_config(route_name='folders_new', renderer='json', request_method='POST')
def folder_create(req: Request):
    folder = folders_crud.create(req)
    if not folder:
        return httpexceptions.HTTPConflict('folder already exist')
    return folder


@view_config(route_name='folders', renderer='json', request_method='GET')
def folder_read(req: Request):
    folder = folders_crud.read(req)
    if not folder:
        return httpexceptions.HTTPNotFound()
    return folder


@view_config(route_name='folders_all', renderer='json', request_method='GET')
def folder_read_all(req: Request):
    folders = folders_crud.read_all()
    return folders


@view_config(route_name='folders', renderer='json', request_method='PUT')
def folder_update(req: Request):
    folder = folders_crud.update(req)
    if not folder:
        return httpexceptions.HTTPNotFound()
    return folder


@view_config(route_name='folders', renderer='json', request_method='DELETE')
def folder_delete(req: Request):
    folder = folders_crud.delete(req)
    if not folder:
        return httpexceptions.HTTPNotFound()
    return folder


# ToDo
@view_config(route_name='registry', renderer='string', request_method='POST')
def registry(req: Request):
    user = user_crud.create(req)
    return {
        'id': user.id,
        'name': user.name,
        'password': user.password,
        'created_at': user.created_at
    }


# ToDo
@view_config(route_name='login', renderer='string', request_method='POST')
def login(req: Request):
    pass


@view_config(route_name='files_new', renderer='string', request_method='POST')
def file_upload(req: Request):
    file = files_crud.create(req)
    if not file:
        return 'file already exist'
    return {'file_name': file.file_name,
            'id': file.id,
            'folder_id': file.folder_id,
            'size': file.size,
            'type': file.type,
            'created_at': file.created_at,
            'updated_at': file.updated_at}


@view_config(route_name='files', request_method='GET')
def file_download(req: Request):
    file_name, file = files_crud.read(req)
    if not file:
        return httpexceptions.HTTPNotFound()
    res = Response(body=file.data)
    res.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name
    return res


@view_config(route_name='files', renderer='string', request_method='PUT')
def file_move(req: Request):
    file = files_crud.move(req)
    if not file:
        return httpexceptions.HTTPNotFound()
    return file


@view_config(route_name='files', renderer='string', request_method='PATCH')
def file_rename(req: Request):
    file = files_crud.update(req)
    return {'file_name': file.file_name,
            'id': file.id,
            'folder_id': file.folder_id,
            'size': file.size,
            'type': file.type,
            'created_at': file.created_at,
            'updated_at': file.updated_at}


@view_config(route_name='files', renderer='string', request_method='DELETE')
def file_delete(req: Request):
    file = files_crud.delete(req)
    if not file:
        return httpexceptions.HTTPNotFound()
    return file


@view_config(route_name='files_share', renderer='string', request_method='GET')
def file_share_link(req: Request):
    link = files_crud.read_for_share(req)
    if not link:
        return httpexceptions.HTTPNotFound()
    return link


if __name__ == '__main__':
    db.Base.metadata.create_all()
    bucket.init_bucket()

    settings = {
        'debug_all': True,
        'reload_all': True
    }

    config = Configurator(settings=settings)
    config.include('pyramid_debugtoolbar')
    config.add_route('folders', '/folders/{folder_id}')
    config.add_route('folders_new', '/folders_new')
    config.add_route('folders_all', '/folders_all')
    config.add_route('registry', '/registry')
    config.add_route('login', '/login')
    config.add_route('files_new', '/files_new')
    config.add_route('files', '/files/{files_id}')
    config.add_route('files_share', '/files_share/{files_id}')
    config.scan()

    app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
