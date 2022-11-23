from urllib import response
import pytest
import requests

url = "http://localhost:8002"


@pytest.mark.order(1)
def test_get_empty_systems():
    response = requests.get(f"{url}/systems")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body == []


@pytest.mark.order(2)
def test_post_system_one_element():
    tool_to_add = {
        "name": "clang",
        "version_major": 10,
        "purpose": "compiler for x64, x86",
    }

    response = requests.post(f"{url}/systems", json=tool_to_add)
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["identity"] == 1


@pytest.mark.order(3)
def test_get_all_system_one_element():
    response = requests.get(f"{url}/systems")
    assert response.status_code == 200
    response_body = response.json()
    print(response_body)
    print(type(response_body))
    assert response_body[0] == {
        "name": "clang",
        "version_major": 10,
        "purpose": "compiler for x64, x86",
        "identity": 1,
    }
