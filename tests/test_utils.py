from fastapi.utils import get_path_param_names


def test_path_param_names():
    assert get_path_param_names("/") == set()
    assert get_path_param_names("/path/{param}") == {"param"}
    assert get_path_param_names("/path1/{param1}/path2/{param2}") == {"param1", "param2"}
    assert get_path_param_names("/path/{param:path}") == {"param"}
