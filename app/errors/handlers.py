from flask import  request
from app import db
from app.errors import bp

from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']


@bp.app_errorhandler(404)
def not_found_error(error):
    # if wants_json_response():
    return error_response(getattr(error, 'status_code', 404), message=str(error))
    # return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    # if wants_json_response():
    return error_response(500, message=str(error))
    # return render_template('errors/500.html'), 500


@bp.app_errorhandler(Exception)
def defaultHandler(error):
    db.session.rollback()
    # if wants_json_response():
    return error_response(getattr(error, 'status_code', 500), message=str(error))
    # return render_template('errors/500.html'), 500
