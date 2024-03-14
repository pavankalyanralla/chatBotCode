from urllib import response
from flask.json import jsonify

BAD_REQUEST = 400
SUCCESS = 200
CREATED = 201
UNAUTHORIZED = 401
FORBIDDEN = 403
DUPLICATE = 409
EMPTYCONTENT = 204
UPDATED = 202
NOTFOUND = 404
NOTMODIFIED = 304


def successResponse(data):
    response = {
        # 'message':'Fetched Data successfully',
        'data': data,
        'success': True}
    return response, SUCCESS

def masterSuccessResponse(data):
    response = data
    return response, SUCCESS

def failedResponse():
    response = {'message': 'No Record found', 'success': False}
    return response, NOTFOUND

def failedResponsewithMessage(data):
    response = data
    return response, NOTFOUND

def emptyDataResponse():
    response = {
        'message': 'required parameters can not be Empty', 'success': False}
    return response, BAD_REQUEST


def exceptionResponse(data):
    response = {'message': 'exception occured',
                'exception': data, 'success': False}
    return response, NOTFOUND


def exceptionResponseChannel(data):
    response = {'message': 'exception occured', 'exception': data, 'success': False}
    return response, NOTFOUND


def alreadyExistingResponse(name, data):
    response = {'message': ' {} ::: {} already exist'.format(
        name, data), 'success': False}
    return response, DUPLICATE

def alreadyBookmarkResponse(name,data):
    response = {'message': 'postId {} already bookmarked by student, {}'.format(
         name , data), 'success': False}
    return response, DUPLICATE


def dataFetchingErrorResponse(data):
    response = {'message': 'unable to fetch %s' % data, 'success': False}
    return response, BAD_REQUEST


def dataInsertionErrorResponse(data):
    response = {'message': 'unable to insert %s' % data, 'success': False}
    return response, BAD_REQUEST


def dataInsertionSuccessResponse(*data):
    response = {'message': 'successfully created',
                'data': data,
                'success': True
                }
    return response, CREATED


def dataUpdationSuccessResponse(*data):
    response = {'message': 'successfully updated',
                'data': data,
                'success': True
                }
    return response, UPDATED

def dataUpdateSuccessResponse():
    response = {'message': 'successfully updated',

                'success': True
                }
    return response, UPDATED

def dataUpdationFailedResponse(*data):
    response = {'message': 'Failed to update Data',
                'data': data,
                'success': False
                }
    return response, NOTMODIFIED


def dataExistResponse(*data):
    response = {'message': 'Record already Exists',
                'data': data,
                'success': True
                }
    return response, SUCCESS

def incorrectOTPResponse():
    response={'message':'Please enter correct OTP to validate',
              'success':False
              }
    return response,UNAUTHORIZED

def exceptionResponsewithData(data):
    response = {'message': 'exception occured', 'exception': data, 'success': False}
    return response, NOTFOUND

def exceptionResponseWithMessage(data):
    response = {'message': 'exception occured',
                'exception': data, 'success': False}
    return response, NOTFOUND