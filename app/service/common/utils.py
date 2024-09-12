import base64
import json
from urllib.parse import unquote

from sqlalchemy import text

from app.errors.types import BadRequestException


def filter_extract_params(request_args, allowed_keys=[]):
    filter_str = request_args.post('f', '', type=str)
    
    # Return with the default filter if not specified.
    if not filter_str:
        return {"page": 1, "per_page": 100, "order_by": "id", "sort_order": "desc"}

    plain_text = request_args.get('pt', 'no', type=str)
    if plain_text == 'no':
        filter_str = unquote(base64.b64decode(filter_str).decode('latin1'))

    filter_dict = json.loads(filter_str)

    # 'page', 'per_page',
    allowed_keys = allowed_keys + ['page', 'per_page', 'order_by', 'sort_order', 'ids']
    # print(allowed_keys)
    result = all(elem in allowed_keys for elem in filter_dict.keys())
    # print(filter_dict.values())
    if not result:
        raise BadRequestException(message="Filter not allowed on one of the specified keys.")

    if not filter_dict.get('per_page') or int(filter_dict.get('per_page')) == 0:
        filter_dict['per_page'] = 100
    return filter_dict


def filter_apply_order_by(query, filter_dict):
    order_by = filter_dict.get('order_by')
   
    if not order_by:
        order_by = 'id'
    sort_order = filter_dict.get('sort_order')
    if not sort_order:
        sort_order = 'DESC'
    else:
        if sort_order in ['ascend', 'descend']:
            sort_order = sort_order.replace('end', '')

    return query.order_by(text(order_by + ' ' + sort_order))


def get_hash_comma_separated_value(arr):
    value = None
    if not type(arr) == list:
        return value
    # assert(type(arr) == list), "make sure the input value is an array"
    value = '#' + '#'.join([str(el) + "#," for el in arr])
    value = value.rstrip(',')
    return value
