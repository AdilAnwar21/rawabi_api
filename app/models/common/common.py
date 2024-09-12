from datetime import datetime
from math import ceil
import pytz
from sqlalchemy import func
from app import db
from pytz import timezone

IST = pytz.timezone('Asia/Kolkata')


class BaseModel(db.Model):
    __abstract__ = True
    created_on = db.Column(db.DateTime, default=datetime.now(timezone('UTC')))
    updated_on = db.Column(db.DateTime, default=datetime.now(timezone('UTC')), onupdate=datetime.now(timezone('UTC')))


class TenantAwareModel(BaseModel):
    __abstract__ = True
    tenant_name = db.Column(db.String(128), nullable=False)


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, **kwargs):
        paginated_query = query.limit(per_page)
        paginated_query = paginated_query.offset((page - 1) * per_page)
        resources = paginated_query.all()
        # total = get_count(query)
        total = len(query.all())
        total_pages = int(ceil(total / float(per_page)))

        data = {
            'items': [item.to_dict(**kwargs) for item in resources],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': total_pages,
                'total_items': total
            },
        }

        return data




#  Reference:
#  https://gist.github.com/hest/8798884
def get_count(q):
    # print("q value :", q)
    # count_q = q.statement.with_only_columns([]).order_by(None)
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    # print("count_q :", count_q)
    count = q.session.execute(count_q).scalar()
    # print("count :", count)
    return count
