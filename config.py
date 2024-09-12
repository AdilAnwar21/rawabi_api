import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_BASE_DATABASE_URI = os.environ.get('DATABASE_URL')
    SESSION_MAKERS = {}
    SQLALCHEMY_BINDS = {}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 60,
    'pool_pre_ping': True
    }
    # SQLALCHEMY_ECHO = True

    # Email
    

    # Translation
    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')

    # Celery
    broker_url = os.environ.get('broker_url')
    result_backend = os.environ.get('result_backend')
    task_serializer = os.environ.get('task_serializer')
    event_serializer = os.environ.get('event_serializer')
    timezone = os.environ.get('timezone')

    #Misc
    POSTS_PER_PAGE = 25
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'weba', 'm4a', 'ppt', 'pptx',
                          'svg'}

    # STORAGE
    STORAGE_PROVIDER = os.environ.get('STORAGE_PROVIDER')


    # Image sizes (WxH)
    TH_SIZES = [(175, 117), (383, 254)]


    # Flask restplus settings for Swagger
    SWAGGER_UI_DOC_EXPANSION = os.environ.get('RESTX_SWAGGER_UI_DOC_EXPANSION')
    SWAGGER_UI_OPERATION_ID = os.environ.get('RESTX_SWAGGER_UI_OPERATION_ID')
    SWAGGER_UI_REQUEST_DURATION = os.environ.get('RESTX_SWAGGER_UI_REQUEST_DURATION')
    # RESTX_VALIDATE = os.environ.get('RESTX_VALIDATE')
    # RESTX_MASK_SWAGGER = os.environ.get('RESTX_MASK_SWAGGER')
    # RESTX_ERROR_404_HELP = os.environ.get('RESTX_ERROR_404_HELP')
    RECAPTCHA_KEY=os.environ.get('RECAPTCHA_KEY')
