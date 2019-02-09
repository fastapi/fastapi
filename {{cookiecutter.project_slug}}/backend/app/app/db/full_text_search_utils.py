import json
from pathlib import Path, PurePath
from typing import Any, Dict

import requests
from requests.auth import HTTPBasicAuth

from app.core.config import (
    COUCHBASE_FULL_TEXT_INDEX_DEFINITIONS_DIR,
    COUCHBASE_PASSWORD,
    COUCHBASE_USER,
)


def get_index(
    index_name: str,
    *,
    username: str = COUCHBASE_USER,
    password: str = COUCHBASE_PASSWORD,
    host="couchbase",
    port="8094",
):
    full_text_url = f"http://{host}:{port}"
    index_url = f"{full_text_url}/api/index/{index_name}"
    auth = HTTPBasicAuth(username, password)
    response = requests.get(index_url, auth=auth)
    if response.status_code == 400:
        content = response.json()
        error = content.get("error")
        if error == "rest_auth: preparePerms, err: index not found":
            return None
        raise ValueError(error)
    elif response.status_code == 200:
        content = response.json()
        assert (
            content.get("status") == "ok"
        ), "Expected a status OK communicating with Full Text Search"
        index_def = content.get("indexDef")
        return index_def
    raise ValueError(response.text)


def create_index(
    index_definition: Dict[str, Any],
    *,
    reset_uuids=True,
    username: str = COUCHBASE_USER,
    password: str = COUCHBASE_PASSWORD,
    host="couchbase",
    port="8094",
):
    index_name = index_definition.get("name")
    assert index_name, "An index name is required as key in an index definition"
    if reset_uuids:
        index_definition.update({"uuid": "", "sourceUUID": ""})
    full_text_url = f"http://{host}:{port}"
    index_url = f"{full_text_url}/api/index/{index_name}"
    auth = HTTPBasicAuth(username, password)
    response = requests.put(index_url, auth=auth, json=index_definition)
    content = response.json()
    if response.status_code == 400:
        error = content.get("error")
        if (
            "cannot create index because an index with the same name already exists:"
            in error
        ):
            raise ValueError(error)
        else:
            raise ValueError(error)
    elif response.status_code == 200:
        assert (
            content.get("status") == "ok"
        ), "Expected a status OK communicating with Full Text Search"
        return True
    raise ValueError(response.text)


def ensure_create_full_text_indexes(
    index_dir=COUCHBASE_FULL_TEXT_INDEX_DEFINITIONS_DIR,
    username: str = COUCHBASE_USER,
    password: str = COUCHBASE_PASSWORD,
    host="couchbase",
    port="8094",
):
    file_path: PurePath
    for file_path in Path(index_dir).iterdir():
        if file_path.name.endswith(".json"):
            with open(file_path) as f:
                index_definition = json.load(f)
            name = index_definition.get("name")
            assert name, "A full text search index definition must have a name field"
            current_index = get_index(
                index_name=name,
                username=username,
                password=password,
                host=host,
                port=port,
            )
            if not current_index:
                assert create_index(
                    index_definition=index_definition,
                    username=username,
                    password=password,
                    host=host,
                    port=port,
                ), "Full Text Search index could not be created"
