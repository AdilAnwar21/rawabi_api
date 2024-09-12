import logging
import os
from datetime import timedelta
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_cors import CORS
from celery import Celery
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_restx import Api
from flask_seeder import FlaskSeeder
from flask_sqlalchemy import SQLAlchemy
import flask_monitoringdashboard as dashboard

from config import Config

db = SQLAlchemy()
seeder = FlaskSeeder()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()
# Create celery instance.
celery = Celery(__name__, broker=Config.broker_url, backend=Config.result_backend)


#  Create a flask restful API.
authorizations = {
    'api_key': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'basic': {
        'type': 'basic'
    }
}

rplus_api = Api(version='3.0', title='Nidhi API', description='Flask API for the Nidhi application.',
                security=['api_key', 'basic'], authorizations=authorizations, schemes=['https', 'http'])


def filter_description(extra_notes):
    desc = "Returns multiple objects matching the filter criteria. <br><br> \
        This method is invoked with 2 query string parameters. <br><br> \
        <ul>\
            <li>f: Filter, expects a string in JSON format, check the default example for details. This parameter needs to be sent as a JSON string in plain text or base64 based on what is sent as the value for the parameter 'pt'.</li>\
            <li>pt: Plain Text, this indicates whether the query parameter above is sent as plain text or base64 encoded. If set to yes, then the parameter f has to be set in plain text. If set to no, then the parameter f has to be base64 encoded.</li>\
        </ul>"

    extra_desc = '<p>Extra Notes: </p>'
    extra_desc += '<ul>'
    for extra_note in extra_notes:
        extra_desc += '<li>' + extra_note + '</li>'
    extra_desc += '</ul>'

    return desc + extra_desc


def create_app(config_class=Config):
    app = Flask(__name__)
    dashboard.config.init_from(envvar='FLASK_MONITORING_DASHBOARD_CONFIG')
    dashboard.bind(app)
    app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
    app.config.from_object(config_class)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    seeder.init_app(app, db)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    celery.conf.update(app.config)
    # oauth.init_app(app)
    # #
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.models import bp as models_bp
    app.register_blueprint(models_bp)

    from app.api import bp as api_bp
    rplus_api.init_app(api_bp)

    app.register_blueprint(api_bp, url_prefix='/api')
    # if not app.debug and not app.testing:
    #     if app.config['MAIL_SERVER']:
    #         auth = None
    #         if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
    #             auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    #         secure = None
    #         if app.config['MAIL_USE_TLS']:
    #             secure = ()
    #         mail_handler = SMTPHandler(
    #             mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
    #             fromaddr='no-reply@' + app.config['MAIL_SERVER'],
    #             toaddrs=app.config['ADMINS'],
    #             subject='niDhi Failure',
    #             credentials=auth,
    #             secure=secure)
    #         mail_handler.setLevel(logging.ERROR)
    #         app.logger.addHandler(mail_handler)

    #  Enable logging on local also.
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/nidhi.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler)

    # app.logger.setLevel(logging.DEBUG)
    # app.logger.info('EXLYGENZE API Startup')

    # print('encrypt',aesEncrypt('uat-admin@exlygenze.com'))

    return app




from app import models
