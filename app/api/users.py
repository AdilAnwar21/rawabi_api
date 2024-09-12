# from app.service.common.decorators import allowed_users
# from flask import request,  jsonify
# from flask_restx.resource import Resource
# from app.models.user import User

# from flask_restx import fields
# from app import rplus_api, filter_description
# from app.errors.types import BadRequestException, RequestException
# from app.service.common.auth import token_auth
# from app.service.common.session_factory import tenant_session_scope
# from app.service.users import filter_users_service

# ns = rplus_api.namespace('users', description='Operations related to user objects')
# rplus_api.add_namespace(ns)

# dml_object = rplus_api.model('UserObjectCreate', {
#     'username': fields.String(description='The username. Has to be unique.', required=True),
#     'password': fields.String(description='The password.', required=True),
#     'email': fields.String(description='The email. Has to be unique.', required=True),
#     'about_me': fields.String(description='About this user.'),
#     'tenant_name': fields.String(description='The tenant to which this user belongs.', required=True),
#     'user_type': fields.String(description='The user type can be employee, tenant_admin or admin', required=True,
#                                enum=['employee', 'tenant_admin', 'admin'])
# })

# drl_object = rplus_api.inherit('UserObjectRetrieve', dml_object, {
#     'id': fields.Integer(),
#     'created_on': fields.DateTime(),
#     'updated_on': fields.DateTime(),
# })

# filter_args = rplus_api.parser()
# filter_args.add_argument('f', type='str', required=True,
#                          default='{"page": 1, "per_page": 20, "order_by":"id", "sort_order":"desc", "ids":[], "tenant_name":"", "search": ""}')
# filter_args.add_argument('pt', type='str', required=False, default='yes')
# filter_desc = filter_description(extra_notes=[
#     'Filter by "tenant_name" applies an equals search.',
#     'Filter by "search" applies a contains search on the username & email fields of the user object.'
# ])


# @ns.route('/')
# class UserCollection(Resource):
#     @rplus_api.expect(filter_args, validate=True)
#     @rplus_api.doc(description=filter_desc, security='api_key')
#     @token_auth.login_required
#     def get(self):
#         """ Returns multiple objects given the filter. """
#         return jsonify(filter_users_service(request.args))

#     @rplus_api.doc(security=None)
#     @rplus_api.marshal_with(drl_object)
#     @rplus_api.response(201, 'Object successfully created.')
#     @rplus_api.expect(dml_object)
#     def post(self):
#         """ Creates a new object with the specified attributes. """
#         data = request.get_json() or {}
#         if 'username' not in data or 'email' not in data or 'password' not in data:
#             raise BadRequestException('Must include username, email and password fields')

#         print(data)
#         with tenant_session_scope(tenant_name='beevibe_master') as session:
#             if session.query(User).filter_by(username=(data['username'].lower())).first():
#                 raise BadRequestException('Please use a different username')
#             if session.query(User).filter_by(email=(data['email'].lower())).first():
#                 raise BadRequestException('Email address already registered.')

#             user = User()
#             user.is_active = 'yes'
#             user.from_dict(data, new_user=True)
#             session.add(user)
#             session.commit()

#             return user.to_dict(), 201


# @ns.route('/<int:id>')
# class UserItem(Resource):
#     @rplus_api.doc(security='api_key')
#     @rplus_api.marshal_with(drl_object)
#     @rplus_api.response(200, 'Retrieved object')
#     @token_auth.login_required
#     def get(self, id):
#         """ Returns the specified object given its id. """
#         with tenant_session_scope(tenant_name='beevibe_master') as session:
#             entity = session.query(User).get(id)

#             if not entity:
#                 raise RequestException(status_code=404, message="No user found")

#             return entity.to_dict(), 200

#     @rplus_api.doc(security='api_key')
#     @rplus_api.expect(dml_object)
#     @rplus_api.marshal_with(drl_object)
#     @rplus_api.response(200, 'Updated object')
#     @token_auth.login_required
#     @allowed_users(user_types=['admin'])
#     def put(self, id):
#         """ Updates the specified object given its id and payload. """
#         with tenant_session_scope(tenant_name='beevibe_master') as session:
#             user = session.query(User).get(id)

#             if not user:
#                 raise RequestException(status_code=404, message="No user found")

#             data = request.get_json() or {}
#             data['username'] = (data['username'].lower())
#             data['email'] = (data['email'].lower())
#             if 'username' in data and data['username'].strip().lower() != (user.username) and User.query.filter_by(
#                     username=(data['username'].strip().lower())).first():
#                 raise BadRequestException('please use a different username')
#             if 'email' in data and data['email'].strip().lower() != (user.email) and User.query.filter_by(email=(data['email'].strip().lower())).first():
#                 raise BadRequestException('please use a different email address')

#             user.from_dict(data, new_user=False)

#             session.commit()

#         return user.to_dict(), 200


# @ns.route('/me')
# class UserMeItem(Resource):

#     @rplus_api.doc(security='api_key')
#     @rplus_api.doc(description='Returns the currently logged in user.')
#     @rplus_api.response(200, 'Retrieved object')
#     @token_auth.login_required
#     def get(self):
#         """ Returns the currently logged-in user. """
#         current_user = token_auth.current_user()
#         with tenant_session_scope(tenant_name='beevibe_master') as session:
#             entity = session.query(User).get(current_user.id)
#             if not entity:
#                 raise RequestException(status_code=404, message="No user found")

#             ret = entity.to_dict()

#             tenant_obj = session.query(Tenant).filter(Tenant.tenant_name == current_user.tenant_name).first()
#             if tenant_obj:
#                 ret['tenant'] = tenant_obj.to_dict()

#         with tenant_session_scope(tenant_name=ret['tenant_name']) as session:
#             # ret['employee'] = None
#             member = session.query(Member).filter(Member.user_id == ret['id']).first()
#             print(member.to_dict())
#             if member:
#                 ret['member'] = member.to_dict()

#         return jsonify(ret)

