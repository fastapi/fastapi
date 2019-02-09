import uuid
from enum import Enum
from typing import List, Sequence, Type, Union

from pydantic import BaseModel
from pydantic.fields import Field, Shape

from app.core.config import COUCHBASE_BUCKET_NAME
from couchbase.bucket import Bucket
from couchbase.fulltext import MatchAllQuery, QueryStringQuery
from couchbase.n1ql import CONSISTENCY_REQUEST, N1QLQuery


def generate_new_id():
    return str(uuid.uuid4())


def ensure_enums_to_strs(items: Union[Sequence[Union[Enum, str]], Type[Enum]]):
    str_items = []
    for item in items:
        if isinstance(item, Enum):
            str_items.append(str(item.value))
        else:
            str_items.append(str(item))
    return str_items


def get_all_documents_by_type(bucket: Bucket, *, doc_type: str, skip=0, limit=100):
    query_str = f"SELECT *, META().id as id FROM {COUCHBASE_BUCKET_NAME} WHERE type = $type LIMIT $limit OFFSET $skip;"
    q = N1QLQuery(
        query_str, bucket=COUCHBASE_BUCKET_NAME, type=doc_type, limit=limit, skip=skip
    )
    q.consistency = CONSISTENCY_REQUEST
    result = bucket.n1ql_query(q)
    return result


def get_documents_by_keys(
    bucket: Bucket, *, keys: List[str], doc_model=Type[BaseModel]
):
    results = bucket.get_multi(keys, quiet=True)
    docs = []
    for result in results.values():
        doc = doc_model(**result.value)
        docs.append(doc)
    return docs


def results_to_model(results_from_couchbase: list, *, doc_model: Type[BaseModel]):
    items = []
    for doc in results_from_couchbase:
        data = doc[COUCHBASE_BUCKET_NAME]
        doc = doc_model(**data)
        items.append(doc)
    return items


def search_results_to_model(
    results_from_couchbase: list, *, doc_model: Type[BaseModel]
):
    items = []
    for doc in results_from_couchbase:
        data = doc.get("fields")
        if not data:
            continue
        data_nones = {}
        for key, value in data.items():
            field: Field = doc_model.__fields__[key]
            if not value:
                value = None
            elif field.shape in {Shape.LIST, Shape.SET, Shape.TUPLE} and not isinstance(
                value, list
            ):
                value = [value]
            data_nones[key] = value
        doc = doc_model(**data_nones)
        items.append(doc)
    return items


def get_docs(
    bucket: Bucket, *, doc_type: str, doc_model=Type[BaseModel], skip=0, limit=100
):
    doc_results = get_all_documents_by_type(
        bucket, doc_type=doc_type, skip=skip, limit=limit
    )
    return results_to_model(doc_results, doc_model=doc_model)


def get_doc(bucket: Bucket, *, doc_id: str, doc_model: Type[BaseModel]):
    result = bucket.get(doc_id, quiet=True)
    if not result.value:
        return None
    model = doc_model(**result.value)
    return model


def search_docs_get_doc_ids(
    bucket: Bucket,
    *,
    query_string: str,
    index_name: str,
    skip: int = 0,
    limit: int = 100,
):
    query = QueryStringQuery(query_string)
    hits = bucket.search(index_name, query, skip=skip, limit=limit)
    doc_ids = []
    for hit in hits:
        doc_ids.append(hit["id"])
    return doc_ids


def search_get_results(
    bucket: Bucket,
    *,
    query_string: str,
    index_name: str,
    skip: int = 0,
    limit: int = 100,
):
    if query_string:
        query = QueryStringQuery(query_string)
    else:
        query = MatchAllQuery()
    hits = bucket.search(index_name, query, fields=["*"], skip=skip, limit=limit)
    docs = []
    for hit in hits:
        docs.append(hit)
    return docs


def search_get_results_by_type(
    bucket: Bucket,
    *,
    query_string: str,
    index_name: str,
    doc_type: str,
    skip: int = 0,
    limit: int = 100,
):
    type_filter = f"type:{doc_type}"
    if not query_string:
        query_string = type_filter
    if query_string and type_filter not in query_string:
        query_string += f" {type_filter}"
    query = QueryStringQuery(query_string)
    hits = bucket.search(index_name, query, fields=["*"], skip=skip, limit=limit)
    docs = []
    for hit in hits:
        docs.append(hit)
    return docs


def search_docs(
    bucket: Bucket,
    *,
    query_string: str,
    index_name: str,
    doc_model: Type[BaseModel],
    skip=0,
    limit=100,
):
    keys = search_docs_get_doc_ids(
        bucket=bucket,
        query_string=query_string,
        index_name=index_name,
        skip=skip,
        limit=limit,
    )
    if not keys:
        return []
    doc_results = get_documents_by_keys(bucket=bucket, keys=keys, doc_model=doc_model)
    return doc_results


def search_results(
    bucket: Bucket,
    *,
    query_string: str,
    index_name: str,
    doc_model: Type[BaseModel],
    skip=0,
    limit=100,
):
    doc_results = search_get_results(
        bucket=bucket,
        query_string=query_string,
        index_name=index_name,
        skip=skip,
        limit=limit,
    )
    return search_results_to_model(doc_results, doc_model=doc_model)


def search_results_by_type(
    bucket: Bucket,
    *,
    query_string: str,
    index_name: str,
    doc_type: str,
    doc_model: Type[BaseModel],
    skip=0,
    limit=100,
):
    doc_results = search_get_results_by_type(
        bucket=bucket,
        query_string=query_string,
        index_name=index_name,
        doc_type=doc_type,
        skip=skip,
        limit=limit,
    )
    return search_results_to_model(doc_results, doc_model=doc_model)
