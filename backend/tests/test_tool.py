import pytest

from koala.api.document import DocumentApi
from koala.api.system import SystemApi
from koala.api.tool import ToolApi
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
    email_max = "max.muster@email.com"
    api_tool.add_tool(clang)
    api_tool.add_tool(gcc)
    api_user.add_user(UserData(name="muster", first_name="max", email="max.muster@email.com"))
    api_tool.add_tool_owner(tool=clang, owner_email=email_max)
    api_tool.add_tool_owner(tool=gcc, owner_email=email_max)
    tools = api_tool.get_all_tools_owned_by(email_max)
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

    api_tool.add_tool(clang)
    api_tool.add_tool_document(clang, doc_a)
    api_tool.add_tool_document(clang, doc_b)

    result = api_tool.get_tool_documents(clang)
    assert set(result) == set(
        [Document(name="intro", path="path/to/intro"), Document(name="class", path="path/to/class")]
    )


@pytest.mark.skip(reason="Not Implemented")
def test_get_status_for_given_tool():
    pass


@pytest.mark.skip(reason="Not Implemented")
def test_get_number_of_days_left_before_next_periodic_review_for_given_tool():
    pass
