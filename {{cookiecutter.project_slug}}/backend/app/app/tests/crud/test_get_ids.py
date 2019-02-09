from app.crud.user import get_user_doc_id


def test_get_user_id():
    username = "johndoe@example.com"
    user_id = get_user_doc_id(username)
    assert user_id == "userprofile::johndoe@example.com"
