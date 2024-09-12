from app import rplus_api
from app.api import bp

from app.service.common.auth import *
from flask_restx import fields

# auth = HTTPTokenAuth(scheme='Bearer')

ns = rplus_api.namespace('tokens', description='Generate and revoke the bearer tokens.')
rplus_api.add_namespace(ns)
token_object = rplus_api.model('TokenObject', {
    'expires_at': fields.DateTime(description='The token will expire at this datetime.'),
    'token': fields.String(description='The actual token.')
})

# -----------------------------------------------------------------------------------------------------------------------------------------------
# STATUS CODES

LOGGED_IN = 1
LOGGED_OUT = 2
PASS_CHANGE_SUC = 3
PASS_CHANGE_FAIL = 4
AUTH_FAIL = 5
AUTH_SUCC = 6
FIRST_OTP_SUC = 7
OTP_SENT_SUC = 8
OTP_EXP = 9
OTP_VALI = 10
OTP_NOT_CORRECT = 11
WEAK_PASS = 12
JWT_OTP_SEND = 13
ACC_LOCKED = 14
PREV_PASS_USED = 15

OTP_VALIDITY_IN_MINUTE=60*24




# @bp.route('/login', methods=['POST'])
# @basic_auth.login_required
# def multi_otp():
#     user = basic_auth.current_user()
#     tenant = db.session.query(Tenant).filter(Tenant.tenant_name == user.tenant_name).first()
#     return {}


