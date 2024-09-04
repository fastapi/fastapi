from dirty_equals import IsDict
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_text_get():
    response = client.get("/text")
    assert response.status_code == 200, response.text
    assert response.json() == "Hello World"


def test_nonexistent():
    response = client.get("/nonexistent")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Not Found"}


def test_path_foobar():
    response = client.get("/path/foobar")
    assert response.status_code == 200
    assert response.json() == "foobar"


def test_path_str_foobar():
    response = client.get("/path/str/foobar")
    assert response.status_code == 200
    assert response.json() == "foobar"


def test_path_str_42():
    response = client.get("/path/str/42")
    assert response.status_code == 200
    assert response.json() == "42"


def test_path_str_True():
    response = client.get("/path/str/True")
    assert response.status_code == 200
    assert response.json() == "True"


def test_path_int_foobar():
    response = client.get("/path/int/foobar")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "foobar",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }
    )


def test_path_int_True():
    response = client.get("/path/int/True")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "True",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }
    )


def test_path_int_42():
    response = client.get("/path/int/42")
    assert response.status_code == 200
    assert response.json() == 42


def test_path_int_42_5():
    response = client.get("/path/int/42.5")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "42.5",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }
    )


def test_path_float_foobar():
    response = client.get("/path/float/foobar")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "float_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid number, unable to parse string as a number",
                    "input": "foobar",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "value is not a valid float",
                    "type": "type_error.float",
                }
            ]
        }
    )


def test_path_float_True():
    response = client.get("/path/float/True")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "float_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid number, unable to parse string as a number",
                    "input": "True",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "value is not a valid float",
                    "type": "type_error.float",
                }
            ]
        }
    )


def test_path_float_42():
    response = client.get("/path/float/42")
    assert response.status_code == 200
    assert response.json() == 42


def test_path_float_42_5():
    response = client.get("/path/float/42.5")
    assert response.status_code == 200
    assert response.json() == 42.5


def test_path_bool_foobar():
    response = client.get("/path/bool/foobar")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "bool_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid boolean, unable to interpret input",
                    "input": "foobar",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "value could not be parsed to a boolean",
                    "type": "type_error.bool",
                }
            ]
        }
    )


def test_path_bool_True():
    response = client.get("/path/bool/True")
    assert response.status_code == 200
    assert response.json() is True


def test_path_bool_42():
    response = client.get("/path/bool/42")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "bool_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid boolean, unable to interpret input",
                    "input": "42",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "value could not be parsed to a boolean",
                    "type": "type_error.bool",
                }
            ]
        }
    )


def test_path_bool_42_5():
    response = client.get("/path/bool/42.5")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "bool_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid boolean, unable to interpret input",
                    "input": "42.5",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "value could not be parsed to a boolean",
                    "type": "type_error.bool",
                }
            ]
        }
    )


def test_path_bool_1():
    response = client.get("/path/bool/1")
    assert response.status_code == 200
    assert response.json() is True


def test_path_bool_0():
    response = client.get("/path/bool/0")
    assert response.status_code == 200
    assert response.json() is False


def test_path_bool_true():
    response = client.get("/path/bool/true")
    assert response.status_code == 200
    assert response.json() is True


def test_path_bool_False():
    response = client.get("/path/bool/False")
    assert response.status_code == 200
    assert response.json() is False


def test_path_bool_false():
    response = client.get("/path/bool/false")
    assert response.status_code == 200
    assert response.json() is False


def test_path_param_foo():
    response = client.get("/path/param/foo")
    assert response.status_code == 200
    assert response.json() == "foo"


def test_path_param_minlength_foo():
    response = client.get("/path/param-minlength/foo")
    assert response.status_code == 200
    assert response.json() == "foo"


def test_path_param_minlength_fo():
    response = client.get("/path/param-minlength/fo")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "string_too_short",
                    "loc": ["path", "item_id"],
                    "msg": "String should have at least 3 characters",
                    "input": "fo",
                    "ctx": {"min_length": 3},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value has at least 3 characters",
                    "type": "value_error.any_str.min_length",
                    "ctx": {"limit_value": 3},
                }
            ]
        }
    )


def test_path_param_maxlength_foo():
    response = client.get("/path/param-maxlength/foo")
    assert response.status_code == 200
    assert response.json() == "foo"


def test_path_param_maxlength_foobar():
    response = client.get("/path/param-maxlength/foobar")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "string_too_long",
                    "loc": ["path", "item_id"],
                    "msg": "String should have at most 3 characters",
                    "input": "foobar",
                    "ctx": {"max_length": 3},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value has at most 3 characters",
                    "type": "value_error.any_str.max_length",
                    "ctx": {"limit_value": 3},
                }
            ]
        }
    )


def test_path_param_min_maxlength_foo():
    response = client.get("/path/param-min_maxlength/foo")
    assert response.status_code == 200
    assert response.json() == "foo"


def test_path_param_min_maxlength_foobar():
    response = client.get("/path/param-min_maxlength/foobar")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "string_too_long",
                    "loc": ["path", "item_id"],
                    "msg": "String should have at most 3 characters",
                    "input": "foobar",
                    "ctx": {"max_length": 3},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value has at most 3 characters",
                    "type": "value_error.any_str.max_length",
                    "ctx": {"limit_value": 3},
                }
            ]
        }
    )


def test_path_param_min_maxlength_f():
    response = client.get("/path/param-min_maxlength/f")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "string_too_short",
                    "loc": ["path", "item_id"],
                    "msg": "String should have at least 2 characters",
                    "input": "f",
                    "ctx": {"min_length": 2},
                }
            ]
        }
    ) | IsDict(
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value has at least 2 characters",
                    "type": "value_error.any_str.min_length",
                    "ctx": {"limit_value": 2},
                }
            ]
        }
    )


def test_path_param_gt_42():
    response = client.get("/path/param-gt/42")
    assert response.status_code == 200
    assert response.json() == 42


def test_path_param_gt_2():
    response = client.get("/path/param-gt/2")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "greater_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be greater than 3",
                    "input": "2",
                    "ctx": {"gt": 3.0},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value is greater than 3",
                    "type": "value_error.number.not_gt",
                    "ctx": {"limit_value": 3},
                }
            ]
        }
    )


def test_path_param_gt0_0_05():
    response = client.get("/path/param-gt0/0.05")
    assert response.status_code == 200
    assert response.json() == 0.05


def test_path_param_gt0_0():
    response = client.get("/path/param-gt0/0")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "greater_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be greater than 0",
                    "input": "0",
                    "ctx": {"gt": 0.0},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value is greater than 0",
                    "type": "value_error.number.not_gt",
                    "ctx": {"limit_value": 0},
                }
            ]
        }
    )


def test_path_param_ge_42():
    response = client.get("/path/param-ge/42")
    assert response.status_code == 200
    assert response.json() == 42


def test_path_param_ge_3():
    response = client.get("/path/param-ge/3")
    assert response.status_code == 200
    assert response.json() == 3


def test_path_param_ge_2():
    response = client.get("/path/param-ge/2")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "greater_than_equal",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be greater than or equal to 3",
                    "input": "2",
                    "ctx": {"ge": 3.0},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value is greater than or equal to 3",
                    "type": "value_error.number.not_ge",
                    "ctx": {"limit_value": 3},
                }
            ]
        }
    )


def test_path_param_lt_42():
    response = client.get("/path/param-lt/42")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "less_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be less than 3",
                    "input": "42",
                    "ctx": {"lt": 3.0},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value is less than 3",
                    "type": "value_error.number.not_lt",
                    "ctx": {"limit_value": 3},
                }
            ]
        }
    )


def test_path_param_lt_2():
    response = client.get("/path/param-lt/2")
    assert response.status_code == 200
    assert response.json() == 2


def test_path_param_lt0__1():
    response = client.get("/path/param-lt0/-1")
    assert response.status_code == 200
    assert response.json() == -1


def test_path_param_lt0_0():
    response = client.get("/path/param-lt0/0")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "less_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be less than 0",
                    "input": "0",
                    "ctx": {"lt": 0.0},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value is less than 0",
                    "type": "value_error.number.not_lt",
                    "ctx": {"limit_value": 0},
                }
            ]
        }
    )


def test_path_param_le_42():
    response = client.get("/path/param-le/42")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "less_than_equal",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be less than or equal to 3",
                    "input": "42",
                    "ctx": {"le": 3.0},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value is less than or equal to 3",
                    "type": "value_error.number.not_le",
                    "ctx": {"limit_value": 3},
                }
            ]
        }
    )


def test_path_param_le_3():
    response = client.get("/path/param-le/3")
    assert response.status_code == 200
    assert response.json() == 3


def test_path_param_le_2():
    response = client.get("/path/param-le/2")
    assert response.status_code == 200
    assert response.json() == 2


def test_path_param_lt_gt_2():
    response = client.get("/path/param-lt-gt/2")
    assert response.status_code == 200
    assert response.json() == 2


def test_path_param_lt_gt_4():
    response = client.get("/path/param-lt-gt/4")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "less_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be less than 3",
                    "input": "4",
                    "ctx": {"lt": 3.0},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value is less than 3",
                    "type": "value_error.number.not_lt",
                    "ctx": {"limit_value": 3},
                }
            ]
        }
    )


def test_path_param_lt_gt_0():
    response = client.get("/path/param-lt-gt/0")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "greater_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be greater than 1",
                    "input": "0",
                    "ctx": {"gt": 1.0},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value is greater than 1",
                    "type": "value_error.number.not_gt",
                    "ctx": {"limit_value": 1},
                }
            ]
        }
    )


def test_path_param_le_ge_2():
    response = client.get("/path/param-le-ge/2")
    assert response.status_code == 200
    assert response.json() == 2


def test_path_param_le_ge_1():
    response = client.get("/path/param-le-ge/1")
    assert response.status_code == 200


def test_path_param_le_ge_3():
    response = client.get("/path/param-le-ge/3")
    assert response.status_code == 200
    assert response.json() == 3


def test_path_param_le_ge_4():
    response = client.get("/path/param-le-ge/4")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "less_than_equal",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be less than or equal to 3",
                    "input": "4",
                    "ctx": {"le": 3.0},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value is less than or equal to 3",
                    "type": "value_error.number.not_le",
                    "ctx": {"limit_value": 3},
                }
            ]
        }
    )


def test_path_param_lt_int_2():
    response = client.get("/path/param-lt-int/2")
    assert response.status_code == 200
    assert response.json() == 2


def test_path_param_lt_int_42():
    response = client.get("/path/param-lt-int/42")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "less_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be less than 3",
                    "input": "42",
                    "ctx": {"lt": 3},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value is less than 3",
                    "type": "value_error.number.not_lt",
                    "ctx": {"limit_value": 3},
                }
            ]
        }
    )


def test_path_param_lt_int_2_7():
    response = client.get("/path/param-lt-int/2.7")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "2.7",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }
    )


def test_path_param_gt_int_42():
    response = client.get("/path/param-gt-int/42")
    assert response.status_code == 200
    assert response.json() == 42


def test_path_param_gt_int_2():
    response = client.get("/path/param-gt-int/2")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "greater_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be greater than 3",
                    "input": "2",
                    "ctx": {"gt": 3},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value is greater than 3",
                    "type": "value_error.number.not_gt",
                    "ctx": {"limit_value": 3},
                }
            ]
        }
    )


def test_path_param_gt_int_2_7():
    response = client.get("/path/param-gt-int/2.7")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "2.7",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }
    )


def test_path_param_le_int_42():
    response = client.get("/path/param-le-int/42")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "less_than_equal",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be less than or equal to 3",
                    "input": "42",
                    "ctx": {"le": 3},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value is less than or equal to 3",
                    "type": "value_error.number.not_le",
                    "ctx": {"limit_value": 3},
                }
            ]
        }
    )


def test_path_param_le_int_3():
    response = client.get("/path/param-le-int/3")
    assert response.status_code == 200
    assert response.json() == 3


def test_path_param_le_int_2():
    response = client.get("/path/param-le-int/2")
    assert response.status_code == 200
    assert response.json() == 2


def test_path_param_le_int_2_7():
    response = client.get("/path/param-le-int/2.7")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "2.7",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }
    )


def test_path_param_ge_int_42():
    response = client.get("/path/param-ge-int/42")
    assert response.status_code == 200
    assert response.json() == 42


def test_path_param_ge_int_3():
    response = client.get("/path/param-ge-int/3")
    assert response.status_code == 200
    assert response.json() == 3


def test_path_param_ge_int_2():
    response = client.get("/path/param-ge-int/2")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "greater_than_equal",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be greater than or equal to 3",
                    "input": "2",
                    "ctx": {"ge": 3},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value is greater than or equal to 3",
                    "type": "value_error.number.not_ge",
                    "ctx": {"limit_value": 3},
                }
            ]
        }
    )


def test_path_param_ge_int_2_7():
    response = client.get("/path/param-ge-int/2.7")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "2.7",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }
    )


def test_path_param_lt_gt_int_2():
    response = client.get("/path/param-lt-gt-int/2")
    assert response.status_code == 200
    assert response.json() == 2


def test_path_param_lt_gt_int_4():
    response = client.get("/path/param-lt-gt-int/4")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "less_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be less than 3",
                    "input": "4",
                    "ctx": {"lt": 3},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value is less than 3",
                    "type": "value_error.number.not_lt",
                    "ctx": {"limit_value": 3},
                }
            ]
        }
    )


def test_path_param_lt_gt_int_0():
    response = client.get("/path/param-lt-gt-int/0")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "greater_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be greater than 1",
                    "input": "0",
                    "ctx": {"gt": 1},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value is greater than 1",
                    "type": "value_error.number.not_gt",
                    "ctx": {"limit_value": 1},
                }
            ]
        }
    )


def test_path_param_lt_gt_int_2_7():
    response = client.get("/path/param-lt-gt-int/2.7")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "2.7",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }
    )


def test_path_param_le_ge_int_2():
    response = client.get("/path/param-le-ge-int/2")
    assert response.status_code == 200
    assert response.json() == 2


def test_path_param_le_ge_int_1():
    response = client.get("/path/param-le-ge-int/1")
    assert response.status_code == 200
    assert response.json() == 1


def test_path_param_le_ge_int_3():
    response = client.get("/path/param-le-ge-int/3")
    assert response.status_code == 200
    assert response.json() == 3


def test_path_param_le_ge_int_4():
    response = client.get("/path/param-le-ge-int/4")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "less_than_equal",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be less than or equal to 3",
                    "input": "4",
                    "ctx": {"le": 3},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "ensure this value is less than or equal to 3",
                    "type": "value_error.number.not_le",
                    "ctx": {"limit_value": 3},
                }
            ]
        }
    )


def test_path_param_le_ge_int_2_7():
    response = client.get("/path/param-le-ge-int/2.7")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "2.7",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }
    )
