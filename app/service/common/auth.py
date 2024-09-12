import socket
from datetime import datetime
from flask import request
from flask_httpauth import HTTPBasicAuth
from flask_httpauth import HTTPTokenAuth
from app import db
from app import dashboard
from app.errors.types import RequestException
# from app.models.activityLog import ActivityLog
from app.models.user import User
from pytz import timezone

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()
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



# --------------------------------------------------------------------------------
# Crete
# Created by: Remshad M
# User Story/ Task ID:  Basic Authentication
# Date: 01/01/2023
# Purpose of Modification: Account lockout implementation
# --------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------------------------------------
@basic_auth.verify_password
def verify_password(username, password):
    print(username,password)
    user = User.query.filter_by(username=(username.strip().lower())).first()
    now_utc = datetime.now(timezone('UTC'))
    now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
    now_asia = now_asia.replace(tzinfo=None)
    if user and user.login_failed_count >= 5:
        id = user.id
        db.session.commit()
        req_resource = request.url
        browser = str(request.user_agent.browser)
        src_ip = request.headers.get('X-Real-Ip', '0.0.0.0')
        if browser == "None":
            browser = "Postman Testing"
        # my_data = ActivityLog(user_id=id, username=username, datetimestamp=now_asia, req_resource=req_resource,
        #                       src_ip=src_ip, activity=ACC_LOCKED, browser=browser, token=None, token_expiration=None)
        try:
            # db.session.add(my_data)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        raise RequestException(status_code=403, message='Account_locked, Please Reset your password')

    elif user and user.check_password(password):
        print(user.password_expiry)
        if user.password_expiry <= now_asia:
            raise RequestException(status_code=403, message='Password expired, Please reset your password')
        else:
            if user.login_failed_count <= 5:
                user.login_failed_count = 0
                db.session.commit()
                return user
            else:
                id = user.id
                db.session.commit()
                req_resource = request.url
                browser = str(request.user_agent.browser)
                src_ip = request.headers.get('X-Real-Ip', '0.0.0.0')
                if browser == "None":
                    browser = "Postman Testing"
                # my_data = ActivityLog(user_id=id, username=username, datetimestamp=now_asia, req_resource=req_resource,
                #                       src_ip=src_ip, activity=ACC_LOCKED, browser=browser, token=None,
                #                       token_expiration=None)
                try:
                    # db.session.add(my_data)
                    db.session.commit()
                except:
                    db.session.rollback()
                    raise
                raise RequestException(status_code=403, message='Account_locked, Please Reset your password')
    else:
        if user:
            id = user.id
            user.login_failed_count = user.login_failed_count + 1
            db.session.commit()
            date_timestamp = datetime.now()
            req_resource = request.url
            browser = str(request.user_agent.browser)
            src_ip = request.headers.get('X-Real-Ip', '0.0.0.0')
            if browser == "None":
                browser = "Postman Testing"
            # my_data = ActivityLog(user_id=id, username=username, datetimestamp=date_timestamp,
            #                       req_resource=req_resource, src_ip=src_ip, activity=AUTH_FAIL, browser=browser,
            #                       token=None, token_expiration=None)
            try:
                # db.session.add(my_data)
                db.session.commit()
            except:
                db.session.rollback()
                raise
            raise RequestException(status_code=403, message='Password is wrong')
        else:
            id = None
            date_timestamp = datetime.now()
            req_resource = request.url
            browser = str(request.user_agent.browser)
            hostname = str(socket.gethostname())
            src_ip = request.headers.get('X-Real-Ip', '0.0.0.0')
            if browser == "None":
                browser = "Postman Testing"
            # my_data = ActivityLog(user_id=id, username=username, datetimestamp=date_timestamp,
            #                       req_resource=req_resource, src_ip=src_ip, activity=AUTH_FAIL, browser=browser,
            #                       token=None, token_expiration=None)
            try:
                # db.session.add(my_data)
                db.session.commit()
            except:
                db.session.rollback()
                raise
            raise RequestException(status_code=403, message='Username is wrong')


@basic_auth.error_handler
def basic_auth_error(status):
    raise RequestException(status_code=401, message='You are not authorised to access this resource.')


@token_auth.verify_token
def verify_token(token):
    # print("inside the verify token")
    usr=User.check_token(token)
    if usr:
        # dashboard.config.group_by=usr.id
        return usr 
    else: 
        return None


@token_auth.error_handler
def token_auth_error(status):
    raise RequestException(status_code=401, message='You are not authorised to access this resource.')
