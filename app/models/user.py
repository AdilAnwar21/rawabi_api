import base64
import os
from datetime import datetime, timedelta
from hashlib import md5
from time import time
import jwt
from flask import current_app
from flask_login import UserMixin
from pytz import timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.common.common import PaginatedAPIMixin, BaseModel
from app import db,login


class User(PaginatedAPIMixin, UserMixin, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    password_expiry = db.Column(db.DateTime)
    is_active = db.Column(db.String(24), default="no")
    user_type = db.Column(db.String(128))
    tenant_name = db.Column(db.String(64), index=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    #  Required for the API authentication.
    token = db.Column(db.Text)
    token_expiration = db.Column(db.DateTime)
    otp = db.Column(db.String(255))
    otp_date = db.Column(db.DateTime)
    login_failed_count = db.Column(db.Integer, default=0)
    apikey = db.Column(db.String(250), index=True, nullable=True)
    refresh_token = db.Column(db.Text)
    refresh_token_expiry = db.Column(db.DateTime, nullable=True)
    is_otp_authentication_required = db.Column(db.String(5), default='no')
    # For saving temporary password
    temp_password = db.Column(db.Text, nullable=True)
    pwd_mail_sent = db.Column(db.String(24), default="no")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.password_expiry = datetime.utcnow() + timedelta(days=180)

    def check_password(self, password):
        print(generate_password_hash(password))
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.username.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'],
                          algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return

    def get_refresh_token(self, expires_in=60 * 60 * 24):
        now_asia = datetime.now(timezone('Asia/Kolkata'))
        now_asia = now_asia.replace(tzinfo=None)
        # if self.token and self.token_expiration > now + timedelta(seconds=60):
        #     return {
        #         'token': self.token,
        #         'expires_at': self.token_expiration
        #     }
        self.refresh_token = base64.b64encode(os.urandom(256)).decode('utf-8')
        self.refresh_token_expiry = now_asia + timedelta(days=365)
        db.session.add(self)
        db.session.commit()
        return {
            'refresh_token': self.refresh_token,
            'refresh_expires_at': self.refresh_token_expiry
        }

    def get_token(self, expires_in=60 * 60 * 1):
        # now = datetime.utcnow()
        now_asia = datetime.now(timezone('Asia/Kolkata'))
        now_asia = now_asia.replace(tzinfo=None)
        # if self.token and self.token_expiration > now + timedelta(seconds=60):
        #     return {
        #         'token': self.token,
        #         'expires_at': self.token_expiration
        #     }
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now_asia + timedelta(seconds=expires_in)
        db.session.add(self)
        db.session.commit()
        return {
            'token': self.token,
            'expires_at': self.token_expiration
        }

    def revoke_token(self):
        now_asia = datetime.now(timezone('Asia/Kolkata'))
        now_asia = now_asia.replace(tzinfo=None)
        self.token_expiration = now_asia - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        
        if user:
            
            now_asia = datetime.now(timezone('Asia/Kolkata'))
            now_asia = now_asia.replace(tzinfo=None)
            if user.token_expiration <= now_asia:

                return None
            else:
                user.token_expiration = now_asia + timedelta(seconds=60 * 60 * 1)
                db.session.add(user)
                db.session.commit()
                return user
        else:
            print('user not found')
            return None

    def from_dict(self, data, new_user=False):
        for field in ['username', 'tenant_name', 'user_type', 'mobile_login_type',
                      'web_login_type']:
            if field in data:
                if field == 'username':
                    setattr(self, field, (data[field].lower().strip()))
                else:
                    setattr(self, field, data[field])

        if new_user and 'password' in data:
            self.set_password(data['password'])

    def to_dict(self):
        data = {
            'id': self.id,
            'username': (self.username) if self.username else self.username,
            'last_seen': self.last_seen.isoformat() + 'Z',
            'user_type': self.user_type,
            'tenant_name': self.tenant_name,
            'otp': self.otp,
            'otp_date': self.otp_date,
        }
        return data


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
