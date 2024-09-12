# # assign the details of all tenants in the applcation in the tenants variable
from flask import current_app
from app import db


# ip = 'localhost'
# assign the details of all master tenants in the application in the masterTenants variable
masterTenants = [
    {
        'tenant_name': 'investment',
        # 'url': 'mysql://root:open@'+ip+'/nidhi_master',
        'url': current_app.config['SQLALCHEMY_BASE_DATABASE_URI']
    }
]


# function for finding all tenants associated with the application stored in the database
# def getAllTenants():
#     # return masterTenants
#     tenents = db.session.query(Tenant).all()
#     return [{'tenant_name': item.tenant_name, 'url': item.db_connection_string} for item in tenents]