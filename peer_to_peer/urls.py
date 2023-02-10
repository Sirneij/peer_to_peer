import json

from peer_to_peer.handlers import (
    add_money,
    add_user,
    check_balance,
    index,
    transfer_money_out,
    transfer_money_to_user,
)
from peer_to_peer.models import User


def url_handlers(environ, start_reponse, user: User):
    path = environ.get('PATH_INFO')
    if path.endswith('/'):
        path = path[:-1]

    if path == '':
        context = index(environ, user)
        data = json.dumps(context.get('data')) if context.get('data') else json.dumps(context.get('error'))
        status = context['status']

    elif path == '/add-user':
        context = add_user(environ, user)
        data = json.dumps(context.get('data')) if context.get('data') else json.dumps(context.get('error'))
        status = context['status']

    elif path == '/add-money':
        context = add_money(environ, user)
        data = json.dumps(context.get('data')) if context.get('data') else json.dumps(context.get('error'))
        status = context['status']
    elif path == '/check-balance':
        context = check_balance(environ, user)
        data = json.dumps(context.get('data')) if context.get('data') else json.dumps(context.get('error'))
        status = context['status']
    elif path == '/transfer-money-to-user':
        context = transfer_money_to_user(environ, user)
        data = json.dumps(context.get('data')) if context.get('data') else json.dumps(context.get('error'))
        status = context['status']
    elif path == '/transfer-money-out':
        context = transfer_money_out(environ, user)
        data = json.dumps(context.get('data')) if context.get('data') else json.dumps(context.get('error'))
        status = context['status']
    else:
        data, status = json.dumps({'error': '404 Not Found'}), '400 Not Found'

    data = data.encode('utf-8')
    content_type = 'application/json' if int(status.split(' ')[0]) < 400 else 'text/plain'
    response_headers = [('Content-Type', content_type), ('Content-Length', str(len(data)))]

    start_reponse(status, response_headers)
    return data
