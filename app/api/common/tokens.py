from app import db, rplus_api
from app.service.common.auth import basic_auth
from flask_restx.resource import Resource
from flask_restx import fields

ns = rplus_api.namespace('tokens', description='Generate and revoke the bearer tokens.')
rplus_api.add_namespace(ns)


token_object = rplus_api.model('TokenObject', {
    'expires_at': fields.DateTime(description='The token will expire at this datetime.'),
    'token': fields.String(description='The actual token.')
})


@ns.route('/')
@ns.route('')
class Tokens(Resource):

    @rplus_api.doc(security='basic')
    @rplus_api.marshal_with(token_object)
    @basic_auth.login_required
    def post(self):
        print(basic_auth.current_user())
        token_info = basic_auth.current_user().get_token()
        db.session.commit()
        token_info["expires_at"] = token_info["expires_at"].replace(microsecond=0).isoformat()
        # jwt_token = jwt.encode({'username': user.username,'exp' : datetime.utcnow() + timedelta(seconds= 60) }, "ThisIsABigSecret")
        return token_info, 200

    @rplus_api.doc(security='api_key')
    # @token_auth.login_required
    def delete(self):
        # token_auth.current_user().revoke_token()
        # db.session.commit()
        return None, 200
