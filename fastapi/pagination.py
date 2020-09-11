from typing import List, Any, Iterable

from pydantic import BaseModel, Field
from starlette.requests import Request


class PaginationParam(object):
    """
    base pagination param
    every page_mode that used have to inherit this class
    """
    page_size = 10
    max_page_size = 100
    min_page_size = 5
    page_size_query_param: str = 'page_size'
    page_query_param: str = 'page_num'


class Pagination(BaseModel):
    """
    pagination model
    """
    count: int = Field(0, ge=0)
    next: str = None
    previous: str = None
    results: list = []


def get_pagination(response_model: BaseModel):
    # produce the pagination model

    if response_model is None:
        return Pagination
    elif issubclass(response_model, Pagination):
        return response_model

    class _Pagination(Pagination):
        results: List[response_model] = []

    return _Pagination


def handle_error_struct(data: Any):
    # handle the data format when it's illegal
    try:
        return {'results': [dict(data)], 'count': 1, 'next': None, 'previous': None}
    except ValueError:
        return {'results': [data], 'count': 1, 'next': None, 'previous': None}


def page_split(request: Request, page_field: PaginationParam, raw_response: Iterable):
    try:
        # get the pagination info
        page_num = int(request.query_params.get(page_field.page_query_param, 1))
        page_size = int(request.query_params.get(page_field.page_size_query_param, page_field.page_size))
    except ValueError as e:
        raise ValueError(f'{page_field.page_query_param} and {page_field.page_size_query_param} requires integer type')
    # check the values
    if page_size > page_field.max_page_size or page_size < page_field.min_page_size or page_size <= 0:
        raise ValueError(
            f'{page_field.page_size_query_param} should between {page_field.max_page_size} and {page_field.min_page_size} and bigger than 0')
    if page_num <= 0:
        raise ValueError(f'{page_field.page_size_query_param} should bigger than 0!')
    # produce url
    base_url = f'{request.url.scheme}://{request.url.netloc}{request.url.path}'
    query_params = dict(request.query_params.items())
    if page_num == 1:
        previous_url = None
    else:
        query_params[page_field.page_query_param] = page_num-1
        previous_url = f'{base_url}?{"&".join([f"{key}={value}" for key,value in query_params.items()])}'
    if page_size * page_num >= len(raw_response):
        next_url = None
    else:
        query_params[page_field.page_query_param] = page_num+1
        next_url = f'{base_url}?{"&".join([f"{key}={value}" for key,value in query_params.items()])}'
    # format the data
    return {'count': len(raw_response), 'next': next_url, 'previous': previous_url,
            'results': raw_response[(page_num - 1) * page_size:page_num * page_size]}
