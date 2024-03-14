from flask import Flask, jsonify
from flask import *
from flask_restful import Api
from flask_restful import Resource, reqparse


errors = {
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': 404,
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 410,
        'extra': "Any extra information you want.",
    },
    '400': {
        'message': "A user with that username already exists.",
        'status': 400,
    },
}


def handle_error(error):
    message = [str(x) for x in error.args]
    status_code = 500
    success = False
    response = {
        'success': success,
        'error': {
            'type': error.__class__.__name__,
            'message': message
        }
    }

    return jsonify(response), status_code
