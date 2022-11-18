import os

import pytest
from dependency_injector import providers

from koala.api.api import Api, Document, System, Tool
from koala.api.user import UserApi, UserData
from koala.factory import ContainerApi, ContainerDatabase

host = os.getenv("IMMUDB_HOST", "database")
print(f"DATABASE: {host}")
URL = f"{host}:3322"
USERNAME = "immudb"
PASSWORD = "immudb"


@pytest.fixture(scope="function")
def koala_api(request):
    config = providers.Configuration()
    database_name = request.node.name.replace("_", "")
    config.from_dict(
        {
            "database": {"url": URL, "name": database_name, "username": USERNAME, "password": PASSWORD},
        },
    )
    database_container = ContainerDatabase(config=config)
    api_container = ContainerApi(config=config, immuclient=database_container.immuclient)
    immuclient = database_container.immuclient()
    immuclient.login(username=USERNAME, password=PASSWORD)
    database = database_container.database()
    database.delete()
    database.create_and_use()
    database.setup_tables()
    yield api_container
    database.delete()
    client = database_container.immuclient()
    client.logout()
    client.shutdown()


def test_get_all_sdes_returns_none_when_empty(koala_api):
    api = koala_api.api_factory()
    assert api.get_all_systems() == []


def test_add_one_sde(koala_api):
    api = koala_api.api_factory()
    esw1 = System(name="eSW", version_major=1, purpose="building firmware")
    api.add_system(esw1)
    all_sdes = api.get_all_systems()
    print(all_sdes)
    assert set(all_sdes) == set([esw1])


def test_add_two_sdes_same_name_and_purpose_different_versions(koala_api):
    api = koala_api.api_factory()
    esw1 = System(name="eSW", version_major=1, purpose="building firmware")
    api.add_system(esw1)

    esw2 = System(name="eSW", version_major=2, purpose="building firmware")
    api.add_system(esw2)

    all_sdes = api.get_all_systems()
    assert set(all_sdes) == set([esw1, esw2])


def test_get_all_tools_return_none_when_empty(koala_api):
    api = koala_api.api_factory()
    assert api.get_all_tools() == []


def test_add_one_tool(koala_api):
    api = koala_api.api_factory()
    gcc = Tool(name="gcc", version_major=14, purpose="compiler")
    api.add_tool(gcc)

    all_tools = api.get_all_tools()
    assert set(all_tools) == set([gcc])


def test_add_one_tool_with_different_versions(koala_api):
    api = koala_api.api_factory()
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
    api = koala_api.api_factory()
    clang_host = Tool(name="clang", version_major=10, purpose="host compiler")
    api.add_tool(clang_host)

    clang_target = Tool(name="clang", version_major=10, purpose="target compiler")
    api.add_tool(clang_target)

    all_tools = api.get_all_tools()
    assert set(all_tools) == set([clang_host, clang_target])


def test_add_one_tool_with_different_version_different_purposes(koala_api):
    api = koala_api.api_factory()
    clang_host = Tool(name="clang", version_major=10, purpose="host compiler")
    api.add_tool(clang_host)

    clang_target = Tool(name="clang", version_major=11, purpose="target compiler")
    api.add_tool(clang_target)

    all_tools = api.get_all_tools()
    assert set(all_tools) == set([clang_host, clang_target])


def test_add_two_tools(koala_api):
    api = koala_api.api_factory()
    gcc = Tool(name="gcc", version_major=14, purpose="compiler")
    api.add_tool(gcc)

    clang = Tool(name="clang", version_major=12, purpose="compiler")
    api.add_tool(clang)

    all_tools = api.get_all_tools()
    assert set(all_tools) == set([gcc, clang])


def test_get_tools_with_given_name_when_one_tool_2_versions_and_purposes(koala_api):
    api = koala_api.api_factory()
    clang_host = Tool(name="clang", version_major=10, purpose="host compiler")
    api.add_tool(clang_host)

    clang_target = Tool(name="clang", version_major=11, purpose="target compiler")
    api.add_tool(clang_target)

    tools = api.get_tools(name="clang")
    assert set(tools) == set([clang_host, clang_target])


def test_get_tools_with_given_name_when_one_tool_1_versions_and_2_purposes(koala_api):
    api = koala_api.api_factory()
    clang_host = Tool(name="clang", version_major=10, purpose="host compiler")
    api.add_tool(clang_host)

    clang_target = Tool(name="clang", version_major=10, purpose="target compiler")
    api.add_tool(clang_target)

    tools = api.get_tools(name="clang")
    assert set(tools) == set([clang_host, clang_target])


def test_get_tool_for_system_when_empty(koala_api):
    api = koala_api.api_factory()
    esw1 = System(name="eSW", version_major=1, purpose="building firmware")
    tools = api.get_tools_for_system(esw1)
    assert tools == []


def test_link_existing_tool_to_existing_sde(koala_api):
    api = koala_api.api_factory()
    esw1 = System(name="eSW", version_major=1, purpose="building firmware")
    api.add_system(esw1)

    gcc = Tool(name="gcc", version_major=14, purpose="compiler")
    api.add_tool(gcc)

    clang = Tool(name="clang", version_major=13, purpose="compiler")
    api.add_tool(clang)

    api.link_tools_to_system(tools=[gcc, clang], system=esw1)

    tools = api.get_tools_for_system(esw1)
    assert set(tools) == set([gcc, clang])


def test_link_existing_sde_to_existing_tool(koala_api):
    api = koala_api.api_factory()
    esw1 = System(name="eSW", version_major=1, purpose="building firmware")
    api.add_system(esw1)

    project_x = System(name="project x", version_major=1, purpose="building firmware for project X")
    api.add_system(project_x)

    project_y = System(name="project y", version_major=2, purpose="building firmware for project Y")
    api.add_system(project_y)

    gcc = Tool(name="gcc", version_major=14, purpose="compiler")
    api.add_tool(gcc)

    api.link_tools_to_system(tools=[gcc], system=esw1)
    api.link_tools_to_system(tools=[gcc], system=project_x)

    systems = api.get_systems_for_tool(gcc)
    assert set(systems) == set([esw1, project_x])


def test_get_all_tools_not_in_any_sde(koala_api):
    api = koala_api.api_factory()
    esw1 = System(name="eSW", version_major=1, purpose="building firmware")
    api.add_system(esw1)

    gcc = Tool(name="gcc", version_major=14, purpose="compiler")
    api.add_tool(gcc)

    clang = Tool(name="clang", version_major=13, purpose="compiler")
    api.add_tool(clang)

    api.link_tools_to_system(tools=[gcc], system=esw1)

    result = api.unlinked_tools()
    assert len(result) == 1
    assert set(result) == set([clang])

    ide = Tool(name="ide", version_major=12, purpose="IDE", gmp_relevant=False)
    api.add_tool(ide)
    relevant_gmp_tools = api.get_gmp_relevant_tools()
    assert len(relevant_gmp_tools) == 2
    assert set(relevant_gmp_tools) == set([gcc, clang])


def test_get_all_non_gmp_relevant_tools(koala_api):
    api = koala_api.api_factory()
    gcc = Tool(name="gcc", version_major=14, purpose="compiler")
    api.add_tool(gcc)

    clang = Tool(name="clang", version_major=13, purpose="compiler")
    api.add_tool(clang)

    ide = Tool(name="ide", version_major=12, purpose="IDE", gmp_relevant=False)
    api.add_tool(ide)
    relevant_non_gmp_tools = api.get_non_gmp_relevant_tools()
    assert len(relevant_non_gmp_tools) == 1
    assert set(relevant_non_gmp_tools) == set([ide])


def test_submit_change_for_given_user_and_given_tool():
    pass


def test_submit_change_for_given_user_and_given_sde():
    pass


def test_user_approves_given_change():
    pass


def test_user_refuses_given_change():
    pass


def test_get_all_changes_for_given_tool():
    pass


def test_get_all_changes_for_given_tool_between_date1_and_date2():
    pass


def test_get_all_changes_for_given_sde_between_date1_and_date2():
    pass


def test_get_all_tools_owned_by_given_user(koala_api):
    api: Api = koala_api.api_factory()
    api_user: UserApi = koala_api.api_user_factory()

    clang = Tool(name="clang", version_major=13, purpose="compiler")
    gcc = Tool(name="gcc", version_major=14, purpose="compiler")
    email_max = "max.muster@email.com"
    api.add_tool(clang)
    api.add_tool(gcc)
    api_user.add_user(UserData(name="muster", first_name="max", email="max.muster@email.com"))
    api.add_tool_owner(tool=clang, owner_email=email_max)
    api.add_tool_owner(tool=gcc, owner_email=email_max)
    tools = api.get_all_tools_owned_by(email_max)
    assert len(tools) == 2
    assert set(tools) == set([gcc, clang])


def test_get_all_sdes_owned_by_given_user():
    pass


def test_get_all_documents_for_given_tool(koala_api):
    api = koala_api.api_factory()
    clang = Tool(name="clang", version_major=13, purpose="compiler")
    spec_a = {"name": "intro", "path": "path/to/intro"}
    spec_b = {"name": "class", "path": "path/to/class"}

    doc_a = Document(**spec_a)
    doc_b = Document(**spec_b)

    api.add_document(doc_a)
    api.add_document(doc_b)

    api.add_tool(clang)
    api.add_tool_document(clang, doc_a)
    api.add_tool_document(clang, doc_b)

    result = api.get_tool_documents(clang)
    assert set(result) == set(
        [Document(name="intro", path="path/to/intro"), Document(name="class", path="path/to/class")]
    )


def test_get_all_documents_for_given_sde(koala_api):
    api: Api = koala_api.api_factory()
    esw1 = System(name="esw1", version_major=13, purpose="esw1")
    doc_a = Document(name="intro", path="path/to/intro")
    doc_b = Document(name="class", path="path/to/class")

    api.add_document(doc_a)
    api.add_document(doc_b)

    api.add_system(esw1)
    api.add_system_document(esw1, doc_a)
    api.add_system_document(esw1, doc_b)

    result = api.get_system_documents(esw1)
    assert set(result) == set(
        [Document(name="intro", path="path/to/intro"), Document(name="class", path="path/to/class")]
    )


def test_get_status_for_given_tool():
    pass


def test_get_status_for_given_sde():
    pass


def test_get_number_of_days_left_before_next_periodic_review_for_given_tool():
    pass


def test_get_number_of_days_left_before_next_periodic_review_for_given_sde():
    pass
