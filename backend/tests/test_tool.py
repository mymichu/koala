import pytest

from koala.api.document import DocumentApi
from koala.api.system import SystemApi
from koala.api.tool import ToolApi, ToolStatus
from koala.api.types import Document, System, Tool
from koala.api.user import UserApi, UserData


@pytest.mark.usefixtures("koala_api")
def test_get_all_tools_return_none_when_empty(koala_api):
    api: ToolApi = koala_api.api_tool_factory()
    assert api.get_all_tools() == []


def test_add_one_tool(koala_api):
    api: ToolApi = koala_api.api_tool_factory()
    gcc = Tool(name="gcc", version_major=14, purpose="compiler")
    api.add_tool(gcc)

    all_tools = api.get_all_tools()
    assert set(all_tools) == set([gcc])


def test_add_one_tool_with_different_versions(koala_api):
    api: ToolApi = koala_api.api_tool_factory()
    gcc10 = Tool(name="gcc", version_major=10, purpose="compiler")
    api.add_tool(gcc10)

    gcc11 = Tool(name="gcc", version_major=11, purpose="compiler")
    api.add_tool(gcc11)

    gcc12 = Tool(name="gcc", version_major=12, purpose="compiler")
    api.add_tool(gcc12)

    gcc13 = Tool(name="gcc", version_major=13, purpose="compiler")
    api.add_tool(gcc13)

    all_tools = api.get_all_tools()
    assert set(all_tools) == set([gcc10, gcc11, gcc12, gcc13])


def test_add_one_tool_with_same_version_different_purposes(koala_api):
    api: ToolApi = koala_api.api_tool_factory()
    clang_host = Tool(name="clang", version_major=10, purpose="host compiler")
    api.add_tool(clang_host)

    clang_target = Tool(name="clang", version_major=10, purpose="target compiler")
    api.add_tool(clang_target)

    all_tools = api.get_all_tools()
    assert set(all_tools) == set([clang_host, clang_target])


def test_add_one_tool_with_different_version_different_purposes(koala_api):
    api: ToolApi = koala_api.api_tool_factory()
    clang_host = Tool(name="clang", version_major=10, purpose="host compiler")
    api.add_tool(clang_host)

    clang_target = Tool(name="clang", version_major=11, purpose="target compiler")
    api.add_tool(clang_target)

    all_tools = api.get_all_tools()
    assert set(all_tools) == set([clang_host, clang_target])


def test_add_two_tools(koala_api):
    api: ToolApi = koala_api.api_tool_factory()
    gcc = Tool(name="gcc", version_major=14, purpose="compiler")
    api.add_tool(gcc)

    clang = Tool(name="clang", version_major=12, purpose="compiler")
    api.add_tool(clang)

    all_tools = api.get_all_tools()
    assert set(all_tools) == set([gcc, clang])


def test_get_tools_with_given_name_when_one_tool_2_versions_and_purposes(koala_api):
    api: ToolApi = koala_api.api_tool_factory()
    clang_host = Tool(name="clang", version_major=10, purpose="host compiler")
    api.add_tool(clang_host)

    clang_target = Tool(name="clang", version_major=11, purpose="target compiler")
    api.add_tool(clang_target)

    tools = api.get_tools(name="clang")
    assert set(tools) == set([clang_host, clang_target])


def test_get_tools_with_given_name_when_one_tool_1_versions_and_2_purposes(koala_api):
    api: ToolApi = koala_api.api_tool_factory()
    clang_host = Tool(name="clang", version_major=10, purpose="host compiler")
    api.add_tool(clang_host)

    clang_target = Tool(name="clang", version_major=10, purpose="target compiler")
    api.add_tool(clang_target)

    tools = api.get_tools(name="clang")
    assert set(tools) == set([clang_host, clang_target])


def test_get_tool_for_system_when_empty(koala_api):
    api_system: SystemApi = koala_api.api_system_factory()
    esw1 = System(name="eSW", version_major=1, purpose="building firmware")
    esw1_registered = api_system.add_system(esw1)
    tools = api_system.get_tools_for_system(esw1_registered.identity)
    assert tools == []


def test_link_existing_tool_to_existing_sde(koala_api):
    api_tool: ToolApi = koala_api.api_tool_factory()
    api_system: SystemApi = koala_api.api_system_factory()
    esw1 = System(name="eSW", version_major=1, purpose="building firmware")
    esw1_db = api_system.add_system(esw1)

    gcc = Tool(name="gcc", version_major=14, purpose="compiler")
    gcc_db = api_tool.add_tool(gcc)

    clang = Tool(name="clang", version_major=13, purpose="compiler")
    clang_db = api_tool.add_tool(clang)

    api_tool.link_tools_to_system(tools_id=[gcc_db.identity, clang_db.identity], system_id=esw1_db.identity)

    tools = api_system.get_tools_for_system(esw1_db.identity)
    assert set(tools) == set([gcc, clang])


def test_get_all_tools_not_in_any_sde(koala_api):
    api_tool: ToolApi = koala_api.api_tool_factory()
    api_system: SystemApi = koala_api.api_system_factory()

    esw1 = System(name="eSW", version_major=1, purpose="building firmware")
    esw1_registered = api_system.add_system(esw1)

    gcc = Tool(name="gcc", version_major=14, purpose="compiler")
    gcc_registered = api_tool.add_tool(gcc)

    clang = Tool(name="clang", version_major=13, purpose="compiler")
    api_tool.add_tool(clang)

    api_tool.link_tools_to_system(tools_id=[gcc_registered.identity], system_id=esw1_registered.identity)

    result = api_tool.unlinked_tools()

    assert len(result) == 1
    assert set(result) == set([clang])

    ide = Tool(name="ide", version_major=12, purpose="IDE", gmp_relevant=False)
    api_tool.add_tool(ide)
    relevant_gmp_tools = api_tool.get_gmp_relevant_tools()
    assert len(relevant_gmp_tools) == 2
    assert set(relevant_gmp_tools) == set([gcc, clang])


def test_get_all_non_gmp_relevant_tools(koala_api):
    api_tool: ToolApi = koala_api.api_tool_factory()

    gcc = Tool(name="gcc", version_major=14, purpose="compiler")
    api_tool.add_tool(gcc)

    clang = Tool(name="clang", version_major=13, purpose="compiler")
    api_tool.add_tool(clang)

    ide = Tool(name="ide", version_major=12, purpose="IDE", gmp_relevant=False)
    api_tool.add_tool(ide)
    relevant_non_gmp_tools = api_tool.get_non_gmp_relevant_tools()
    assert len(relevant_non_gmp_tools) == 1
    assert set(relevant_non_gmp_tools) == set([ide])


@pytest.mark.skip(reason="Not Implemented")
def test_submit_change_for_given_user_and_given_tool():
    pass


@pytest.mark.skip(reason="Not Implemented")
def test_get_all_changes_for_given_tool():
    pass


@pytest.mark.skip(reason="Not Implemented")
def test_get_all_changes_for_given_tool_between_date1_and_date2():
    pass


def test_get_all_tools_owned_by_given_user(koala_api):
    api_tool: ToolApi = koala_api.api_tool_factory()
    api_user: UserApi = koala_api.api_user_factory()

    clang = Tool(name="clang", version_major=13, purpose="compiler")
    gcc = Tool(name="gcc", version_major=14, purpose="compiler")
    clang_registered = api_tool.add_tool(clang)
    gcc_registered = api_tool.add_tool(gcc)
    registered_user = api_user.add_user(UserData(name="muster", first_name="max", email="max.muster@email.com"))
    api_tool.add_tool_owner(tool_id=clang_registered.identity, owner_id=registered_user.identity)
    api_tool.add_tool_owner(tool_id=gcc_registered.identity, owner_id=registered_user.identity)
    tools = api_tool.get_all_tools_owned_by(registered_user.identity)
    assert len(tools) == 2
    assert set(tools) == set([gcc, clang])


def test_get_all_documents_for_given_tool(koala_api):
    api_tool: ToolApi = koala_api.api_tool_factory()
    api_document: DocumentApi = koala_api.api_document_factory()
    clang = Tool(name="clang", version_major=13, purpose="compiler")
    spec_a = {"name": "intro", "path": "path/to/intro"}
    spec_b = {"name": "class", "path": "path/to/class"}

    doc_a = Document(**spec_a)
    doc_b = Document(**spec_b)

    api_document.add_document(doc_a)
    api_document.add_document(doc_b)

    clang_registered = api_tool.add_tool(clang)
    api_tool.add_tool_document(clang_registered.identity, doc_a)
    api_tool.add_tool_document(clang_registered.identity, doc_b)

    result = api_tool.get_tool_documents(clang_registered.identity)
    assert set(result) == set(
        [Document(name="intro", path="path/to/intro"), Document(name="class", path="path/to/class")]
    )


def test_get_status_for_given_tool(koala_api):
    api_tool: ToolApi = koala_api.api_tool_factory()
    api_document: DocumentApi = koala_api.api_document_factory()
    clang = Tool(name="clang", version_major=10, purpose="compiler")
    doc_a = Document(name="intro", path="path/to/intro")
    doc_b = Document(name="class", path="path/to/class")

    clang_registered = api_tool.add_tool(clang)
    api_document.add_document(doc_a)
    api_document.add_document(doc_b)
    api_tool.add_tool_document(clang_registered.identity, doc_a)
    api_tool.add_tool_document(clang_registered.identity, doc_b)

    result = api_tool.get_tool_status(clang_registered.identity)

    assert (
        ToolStatus(
            is_productive=False,
            amount_documents_released=0,
            amount_documents_unreleased=2,
            amount_change_requests_closed=0,
            amount_change_requests_open=0,
        )
        == result
    )


def test_get_status_for_given_tool_productive(koala_api):
    api_tool: ToolApi = koala_api.api_tool_factory()
    api_document: DocumentApi = koala_api.api_document_factory()
    clang = Tool(name="clang", version_major=10, purpose="compiler")
    doc_a = Document(name="intro", path="path/to/intro")
    doc_b = Document(name="class", path="path/to/class")

    clang_registered = api_tool.add_tool(clang)
    doc_a_registered = api_document.add_document(doc_a)
    doc_b_registered = api_document.add_document(doc_b)
    api_tool.add_tool_document(clang_registered.identity, doc_a)
    api_tool.add_tool_document(clang_registered.identity, doc_b)

    api_document.update_release_status(doc_a_registered.identity, True)
    api_document.update_release_status(doc_b_registered.identity, True)
    api_tool.set_tool_productive(clang_registered.identity)
    result = api_tool.get_tool_status(clang_registered.identity)

    assert (
        ToolStatus(
            is_productive=True,
            amount_documents_released=2,
            amount_documents_unreleased=0,
            amount_change_requests_closed=0,
            amount_change_requests_open=0,
        )
        == result
    )


@pytest.mark.skip(reason="Not Implemented")
def test_get_number_of_days_left_before_next_periodic_review_for_given_tool():
    pass
