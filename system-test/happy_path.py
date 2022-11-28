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
    assert response_body[0] == {
        "name": "system 1",
        "version_major": 1,
        "purpose": "toolchain for embedded systems",
        "identity": 1,
    }


@pytest.mark.order(4)
def test_get_system_status_1_no_elements() -> None:
    response = requests.get(f"{url}/systems/1")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body == {
        "is_productive": False,
        "amount_documents_released": 0,
        "amount_documents_unreleased": 0,
        "amount_tools_productive": 0,
        "amount_tools_not_productive": 0,
        "amount_systems_productive": 0,
        "amount_systems_not_productive": 0,
        "amount_change_requests_closed": 0,
        "amount_change_requests_open": 0,
    }


@pytest.mark.order(5)
def test_post_document_to_system_1() -> None:
    doc_to_add = {"name": "test-doc", "path": "test-path"}

    response = requests.post(f"{url}/systems/1/documents", json=doc_to_add)
    assert response.status_code == 200
    response_body = response.json()
    assert response_body == {"name": "test-doc", "path": "test-path", "identity": 1}


@pytest.mark.order(6)
def test_get_system_status_1_1_document_not_released() -> None:
    response = requests.get(f"{url}/systems/1")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body == {
        "is_productive": False,
        "amount_documents_released": 0,
        "amount_documents_unreleased": 1,
        "amount_tools_productive": 0,
        "amount_tools_not_productive": 0,
        "amount_systems_productive": 0,
        "amount_systems_not_productive": 0,
        "amount_change_requests_closed": 0,
        "amount_change_requests_open": 0,
    }


@pytest.mark.order(7)
def test_put_document_1_to_release() -> None:
    response = requests.put(f"{url}/documents/1/state?state=relased")
    assert response.status_code == 200


@pytest.mark.order(8)
def test_get_system_status_1_1_document_released() -> None:
    response = requests.get(f"{url}/systems/1")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body == {
        "is_productive": False,
        "amount_documents_released": 1,
        "amount_documents_unreleased": 0,
        "amount_tools_productive": 0,
        "amount_tools_not_productive": 0,
        "amount_systems_productive": 0,
        "amount_systems_not_productive": 0,
        "amount_change_requests_closed": 0,
        "amount_change_requests_open": 0,
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


@pytest.mark.order(19)
def test_check_link_arm_compiler_to_clang():
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


@pytest.mark.order(20)
def test_check_get_status_tool_no_documents():
    response = requests.get(f"{url}/tools/2")
    assert response.status_code == 200
    assert response.json() == {
        "is_productive": False,
        "amount_documents_released": 0,
        "amount_documents_unreleased": 0,
        "amount_change_requests_closed": 0,
        "amount_change_requests_open": 0,
    }


@pytest.mark.order(21)
def test_post_document_to_tools_1():
    doc_to_add = {"name": "test-doc-tool", "path": "test-path-tool"}

    response = requests.post(f"{url}/tools/2/documents", json=doc_to_add)
    assert response.status_code == 200
    assert response.json() == {
        "name": "test-doc-tool",
        "path": "test-path-tool",
        "identity": 2,
    }


@pytest.mark.order(22)
def test_check_get_status_tool_added_documentsdasdass():
    response = requests.get(f"{url}/tools/2")
    assert response.json() == {
        "is_productive": False,
        "amount_documents_released": 0,
        "amount_documents_unreleased": 1,
        "amount_change_requests_closed": 0,
        "amount_change_requests_open": 0,
    }


@pytest.mark.order(23)
def test_post_add_usr():
    user = {"name": "Muster", "first_name": "Max", "email": "max.muster@email.com"}

    response = requests.post(f"{url}/user", json=user)
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["identity"] == 1


@pytest.mark.order(24)
def test_link_systems_tools_and_get_status():
    # link tool clang with max-muster
    requests.post(f"{url}/tools/2/owner?owner_identity=1")
    # link system 1 with max-muster
    requests.post(f"{url}/systems/1/owner?owner_identity=1")
    response = requests.get(f"{url}/user/1")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body == {
        "name": "Muster",
        "first_name": "Max",
        "email": "max.muster@email.com",
        "active": True,
        "identity": 1,
        "ownership": {
            "systems": [
                {
                    "name": "system 1",
                    "version_major": 1,
                    "purpose": "toolchain for embedded systems",
                    "identity": 1,
                }
            ],
            "tools": [
                {
                    "name": "clang",
                    "purpose": "compiler for x84/64 processors",
                    "version_major": 10,
                    "gmp_relevant": True,
                    "identity": 2,
                }
            ],
        },
    }


@pytest.mark.order(25)
def test_post_add_change_to_clang():
    user = {"entity_id": 2, "requester_id": 1, "description": "First Change"}

    response = requests.post(f"{url}/change", json=user)
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["identity"] == 1


@pytest.mark.order(26)
def test_check_get_status_tool_added_change_open():
    response = requests.get(f"{url}/tools/2")
    assert response.json() == {
        "is_productive": False,
        "amount_documents_released": 0,
        "amount_documents_unreleased": 1,
        "amount_change_requests_closed": 0,
        "amount_change_requests_open": 1,
    }


@pytest.mark.order(27)
def test_update_change_reviewer():
    response = requests.put(f"{url}/change/1/reviewer?reviewer_id=1")
    assert response.status_code == 200


@pytest.mark.order(28)
def test_check_get_status_tool_added_change_closed():
    response = requests.get(f"{url}/tools/2")
    assert response.json() == {
        "is_productive": False,
        "amount_documents_released": 0,
        "amount_documents_unreleased": 1,
        "amount_change_requests_closed": 1,
        "amount_change_requests_open": 0,
    }
