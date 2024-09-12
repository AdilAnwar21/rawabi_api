from flask import Blueprint

bp = Blueprint('api', __name__, template_folder='templates')
from .users import *
from .common.tokens import *
