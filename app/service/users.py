from app.models.user import User
from sqlalchemy import or_
from app.service.common import *
from app.service.common.utils import filter_extract_params, filter_apply_order_by
from app.service.common.session_factory import tenant_session_scope
from sqlalchemy import func


def filter_users_service(request_args):
    filter_dict = filter_extract_params(request_args=request_args, allowed_keys=['tenant_name', 'search'])
    ids = filter_dict.get('ids', [])
    tenant_name = filter_dict.get('tenant_name', '')
    search = filter_dict.get('search', '')

    with tenant_session_scope(tenant_name='beevibe_master') as session:

        query = session.query(User)

        if tenant_name:
            query = query.filter(User.tenant_name == tenant_name)

        if search:
            query = query.filter(or_(User.username.like("%{}%".format(search)), User.email.like("%{}%".format(search))))

        if ids:
            query = query.filter(User.id.in_(ids))

        query = filter_apply_order_by(query=query, filter_dict=filter_dict)

        return User.to_collection_dict(query=query, page=filter_dict.get('page', 1), per_page=filter_dict.get('per_page', 100))
