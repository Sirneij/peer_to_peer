from typing import Any
from urllib import parse

from peer_to_peer.models import User


def index(environ, user: User) -> dict[str, Any]:
    """Display the in-memory data to users."""
    request_params = dict(parse.parse_qsl(parse.urlsplit(environ.get('RAW_URI')).query))

    context = {'status': '200 Ok'}
    if request_params and request_params.get('name').replace('\'', '').lower() == 'admin':
        user_data = user.user_data
        for data in user_data:
            if data:
                if data.get('password'):
                    data.pop('password')
        context['data'] = user_data

    elif request_params and request_params.get('name').replace('\'', '').lower():
        current_user = user.return_user(request_params.get('name').replace('\'', '').lower())
        context['data'] = current_user

    else:
        context['data'] = 'You cannot just view this page without a `name` query parameter.'
    return context


def add_user(environ, user: User) -> dict[str, Any]:
    """Use query parameters to add users to the in-memory data."""

    if parse.parse_qsl(parse.urlsplit(environ.get('RAW_URI')).query) == '':
        return {'error': '405 Method Not Allowed', 'status': '405 Method Not Allowed'}
    request_meta_query = dict(parse.parse_qsl(parse.urlsplit(environ.get('RAW_URI')).query))
    if not request_meta_query:
        return {'error': 'Query must be provided.', 'status': '405 Method Not Allowed'}

    user_data = user.user_data
    if not any(d.get('username') == request_meta_query.get('name').replace('\'', '').lower() for d in user_data):
        if all(not data for data in user_data):
            user.set_user_data(
                {
                    'id': 1,
                    'username': request_meta_query.get('name').replace('\'', '').lower(),
                    'password': request_meta_query.get('password'),
                }
            )
        else:
            user.set_user_data(
                {
                    'id': user_data[-1]['id'] + 1,
                    'username': request_meta_query.get('name').replace('\'', '').lower(),
                    'password': request_meta_query.get('password'),
                }
            )

    else:
        return {
            'error': f'A user with username, {request_meta_query.get("name")}, already exists.',
            'status': '409 Conflict',
        }
    context = {'data': user_data[-1], 'status': '200 Ok'}
    return context


def add_money(environ, user: User) -> dict[str, Any]:
    """Use query parameters to add money to a user's account to the in-memory data."""
    if parse.parse_qsl(parse.urlsplit(environ.get('RAW_URI')).query) == '':
        return {'error': '405 Method Not Allowed', 'status': '405 Method Not Allowed'}
    request_meta_query = dict(parse.parse_qsl(parse.urlsplit(environ.get('RAW_URI')).query))
    if not request_meta_query:
        return {'error': 'Query must be provided.', 'status': '405 Method Not Allowed'}

    context = {'status': '200 Ok'}

    user_data = user.return_user(request_meta_query.get('name').replace('\'', '').lower())
    if user_data:
        if user_data['password'] == request_meta_query.get('password'):
            user_data['balance'] = user_data.get('balance', 0.0) + float(request_meta_query.get('amount'))
            context['data'] = user_data
        else:
            return {
                'error': 'You are not authorized to add money to this user\'s balance.',
                'status': '401 Unauthorized',
            }
    else:
        return {'error': 'A user with that name does not exist.', 'status': '404 Not Found'}

    return context


def check_balance(environ, user: User) -> dict[str, Any]:
    """Use query parameters to check a user's account balance to the in-memory data."""
    if parse.parse_qsl(parse.urlsplit(environ.get('RAW_URI')).query) == '':
        return {'error': '405 Method Not Allowed', 'status': '405 Method Not Allowed'}
    request_meta_query = dict(parse.parse_qsl(parse.urlsplit(environ.get('RAW_URI')).query))
    if not request_meta_query:
        return {'error': 'Query must be provided.', 'status': '405 Method Not Allowed'}

    context = {'status': '200 Ok'}

    user_data = user.return_user(request_meta_query.get('name').replace('\'', '').lower())
    if user_data:
        password = request_meta_query.get('password')
        if password:
            if user_data['password'] == password:
                context['data'] = {'balance': user_data.get('balance', 0.0)}
            else:
                return {
                    'error': 'You are not authorized to check this user\'s balance.',
                    'status': '401 Unauthorized',
                }
        else:
            return {
                'error': 'You must provide the user\'s password to check balance.',
                'status': '401 Unauthorized',
            }
    else:
        return {'error': 'A user with that name does not exist.', 'status': '404 Not Found'}
    return context


def transfer_money_to_user(environ, user: User) -> dict[str, Any]:
    """Use query parameters to transfer money from a user to another."""
    if parse.parse_qsl(parse.urlsplit(environ.get('RAW_URI')).query) == '':
        return {'error': '405 Method Not Allowed', 'status': '405 Method Not Allowed'}
    request_meta_query = dict(parse.parse_qsl(parse.urlsplit(environ.get('RAW_URI')).query))
    if not request_meta_query:
        return {'error': 'Query must be provided.', 'status': '405 Method Not Allowed'}

    context = {'status': '200 Ok'}

    user_data = user.return_user(request_meta_query.get('from_name').replace('\'', '').lower())

    if user_data:
        if user_data['password'] == request_meta_query.get('from_password'):
            if request_meta_query.get('amount') and user_data.get('balance', 0.0) >= float(
                request_meta_query.get('amount')
            ):
                beneficiary = user.return_user(request_meta_query.get('to_name').replace('\'', '').lower())
                if beneficiary:
                    beneficiary['balance'] = beneficiary.get('balance', 0.0) + float(request_meta_query['amount'])
                    user_data['balance'] = user_data['balance'] - float(request_meta_query['amount'])
                    context[
                        'data'
                    ] = f'A sum of ${float(request_meta_query["amount"])} was successfully transferred to {request_meta_query.get("to_name")}.'
                else:
                    return {
                        'error': 'The user you want to credit does not exist.',
                        'status': '404 Not Found',
                    }
            else:
                return {
                    'error': 'You either have insufficient funds or did not include `amount` as query parameter.',
                    'status': '404 Not Found',
                }
        else:
            return {
                'error': 'You are not authorized to access this user\'s account.',
                'status': '401 Unauthorized',
            }
    else:
        return {'error': 'A user with that name does not exist.', 'status': '404 Not Found'}
    return context


def transfer_money_out(environ, user: User) -> dict[str, Any]:
    """Use query parameters to transfer money out of this app."""
    if parse.parse_qsl(parse.urlsplit(environ.get('RAW_URI')).query) == '':
        return {'error': '405 Method Not Allowed', 'status': '405 Method Not Allowed'}
    request_meta_query = dict(parse.parse_qsl(parse.urlsplit(environ.get('RAW_URI')).query))
    if not request_meta_query:
        return {'error': 'Query must be provided.', 'status': '405 Method Not Allowed'}

    context = {'status': '200 Ok'}

    user_data = user.return_user(request_meta_query.get('name').replace('\'', '').lower())
    if user_data:
        if user_data.get('password') == request_meta_query.get('password'):
            if request_meta_query.get('amount') and user_data.get('balance') >= float(request_meta_query.get('amount')):
                user_data['balance'] = user_data['balance'] - float(request_meta_query['amount'])
                context[
                    'data'
                ] = f'A sum of ${float(request_meta_query["amount"])} was successfully transferred to {request_meta_query.get("to_bank")}.'
            else:
                return {
                    'error': 'You either have insufficient funds or did not include `amount` as query parameter.',
                    'status': '404 Not Found',
                }
        else:
            return {
                'error': 'You are not authorized to access this user\'s account.',
                'status': '401 Unauthorized',
            }
    else:
        return {'error': 'A user with that name does not exist.', 'status': '404 Not Found'}
    return context
