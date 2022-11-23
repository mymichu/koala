import pytest
import requests


url = "http://localhost:8002"


@pytest.mark.order(1)
def test_get_empty_systems() -> None:
    response = requests.get(f"{url}/systems")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body == []


@pytest.mark.order(2)
def test_post_system_one_element() -> None:
    system_to_add = {
        "name": "system 1",
        "version_major": 1,
        "purpose": "toolchain for embedded systems",
    }

    response = requests.post(f"{url}/systems", json=system_to_add)
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["identity"] == 1


@pytest.mark.order(3)
def test_get_all_system_one_element() -> None:
    response = requests.get(f"{url}/systems")
    assert response.status_code == 200
    response_body = response.json()
    print(response_body)
    print(type(response_body))
    assert response_body[0] == {
        "name": "system 1",
        "version_major": 1,
        "purpose": "toolchain for embedded systems",
        "identity": 1,
    }


@pytest.mark.order(4)
def test_get_system_status_1_no_elements():
    response = requests.get(f"{url}/systems/1")
    assert response.status_code == 200
    response_body = response.json()
    print(response_body)
    print(type(response_body))
    assert response_body == {
        "is_productive": False,
        "amount_documents_released": 0,
        "amount_documents_unreleased": 0,
        "amount_tools_productive": 0,
        "amount_tools_not_productive": 0,
        "amount_systems_productive": 0,
        "amount_systems_not_productive": 0,
        "amount_change_request_closed": 0,
        "amount_change_request_open": 0,
    }


@pytest.mark.order(5)
def test_post_document_to_system_1():
    doc_to_add = {"name": "test-doc", "path": "test-path"}

    response = requests.post(f"{url}/systems/1/documents", json=doc_to_add)
    assert response.status_code == 200
    response_body = response.json()
    assert response_body == {"name": "test-doc", "path": "test-path", "identity": 1}


@pytest.mark.order(6)
def test_get_system_status_1_1_document_not_released():
    response = requests.get(f"{url}/systems/1")
    assert response.status_code == 200
    response_body = response.json()
    print(response_body)
    print(type(response_body))
    assert response_body == {
        "is_productive": False,
        "amount_documents_released": 0,
        "amount_documents_unreleased": 1,
        "amount_tools_productive": 0,
        "amount_tools_not_productive": 0,
        "amount_systems_productive": 0,
        "amount_systems_not_productive": 0,
        "amount_change_request_closed": 0,
        "amount_change_request_open": 0,
    }


@pytest.mark.order(7)
def test_put_document_1_to_release():
    response = requests.put(f"{url}/documents/1/state?state=relased")
    assert response.status_code == 200


@pytest.mark.order(8)
def test_get_system_status_1_1_document_released():
    response = requests.get(f"{url}/systems/1")
    assert response.status_code == 200
    response_body = response.json()
    print(response_body)
    print(type(response_body))
    assert response_body == {
        "is_productive": False,
        "amount_documents_released": 1,
        "amount_documents_unreleased": 0,
        "amount_tools_productive": 0,
        "amount_tools_not_productive": 0,
        "amount_systems_productive": 0,
        "amount_systems_not_productive": 0,
        "amount_change_request_closed": 0,
        "amount_change_request_open": 0,
    }


@pytest.mark.order(9)
def test_get_empty_tools():
    response = requests.get(f"{url}/tools")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body == []


@pytest.mark.order(10)
def test_post_tool_one_element():
    tool_to_add = {
        "name": "clang",
        "purpose": "compiler for x84/64 processors",
        "version_major": 10,
        "gmp_relevant": True,
    }

    response = requests.post(f"{url}/tools", json=tool_to_add)
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["identity"] == 2


@pytest.mark.order(11)
def test_post_tool_second_element():
    tool_to_add = {
        "name": "arm-gcc",
        "purpose": "compiler for arm processors",
        "version_major": 9,
        "gmp_relevant": True,
    }

    response = requests.post(f"{url}/tools", json=tool_to_add)
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["identity"] == 3


@pytest.mark.order(13)
def test_get_two_added_tools():
    response = requests.get(f"{url}/tools")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body == [
        {
            "name": "clang",
            "purpose": "compiler for x84/64 processors",
            "version_major": 10,
            "gmp_relevant": True,
            "identity": 2,
        },
        {
            "name": "arm-gcc",
            "purpose": "compiler for arm processors",
            "version_major": 9,
            "gmp_relevant": True,
            "identity": 3,
        },
    ]


@pytest.mark.order(14)
def test_get_two_added_tools():
    response = requests.get(f"{url}/tools")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body == [
        {
            "name": "clang",
            "purpose": "compiler for x84/64 processors",
            "version_major": 10,
            "gmp_relevant": True,
            "identity": 2,
        },
        {
            "name": "arm-gcc",
            "purpose": "compiler for arm processors",
            "version_major": 9,
            "gmp_relevant": True,
            "identity": 3,
        },
    ]


@pytest.mark.order(15)
def test_no_link_tools_to_esw():
    response = requests.get(f"{url}/systems/1/tools")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.order(16)
def test_no_link_arm_compiler_to_esw1():
    response = requests.get(f"{url}/tools/2/systems")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.order(17)
def test_link_arm_compiler_to_esw1():
    response = requests.post(f"{url}/tools/2/systems?system_identity=1")
    assert response.status_code == 200


@pytest.mark.order(18)
def test_check_link_arm_compiler_to_esw1():
    response = requests.get(f"{url}/tools/2/systems")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "system 1",
            "version_major": 1,
            "purpose": "toolchain for embedded systems",
            "identity": 1,
        }
    ]


@pytest.mark.order(18)
def test_check_link_arm_compiler_to_esw1():
    response = requests.get(f"{url}/systems/1/tools")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "clang",
            "purpose": "compiler for x84/64 processors",
            "version_major": 10,
            "gmp_relevant": True,
            "identity": 2,
        }
    ]
