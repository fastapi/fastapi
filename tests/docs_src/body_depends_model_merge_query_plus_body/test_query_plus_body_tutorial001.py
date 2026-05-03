import pytest
from fastapi import status

from tests.docs_src._loader import docs_src_test_client


@pytest.fixture(scope="module")
def client():
    return docs_src_test_client(
        "docs_src_body_depends_model_merge_query_plus_body_tutorial001",
        "body_depends_model_merge_query_plus_body",
        "tutorial001_an_py310.py",
    )


@pytest.mark.parametrize(
    ("path", "query", "json_body"),
    [
        (
            "/clients/case-files/",
            {"client_id": "rick", "region": "west"},
            {"title": "Q1", "case_number": "C-9"},
        ),
        (
            "/clients/contracts/",
            {"client_id": "morty", "contract_ref": "R-9"},
            {"title": "Partner deal", "contract_id": "Z-1"},
        ),
    ],
    ids=["case_file", "contract"],
)
def test_query_plus_merged_json_body(client, path, query, json_body):
    response = client.post(path, params=query, json=json_body)
    assert response.status_code == status.HTTP_200_OK, response.text
    expected = {
        "client_info": query,
        "record": json_body,
    }
    assert response.json() == expected
