import pytest
from immudb import ImmudbClient
from koala.api import Api, System, Tool
from koala.database.setup import DatabaseInitializer

URL = "database:3322"
USERNAME = "immudb"
PASSWORD = "immudb"


@pytest.fixture(scope="function")
def koala_api(request):
    client = ImmudbClient(URL)
    client.login(USERNAME, PASSWORD)
    database_name = request.node.name
    database_name = database_name.replace("_", "")
    database = DatabaseInitializer(client, database_name)
    # Always make sure we start with a clean database
    database.delete()
    database.create_and_use()
    database.setup_tables()
    api = Api(client)
    yield api
    database.delete()
    client.logout()
    client.shutdown()


def test_get_all_sdes_returns_none_when_empty(koala_api):
    assert koala_api.get_all_systems() == []


def test_add_one_sde(koala_api):
    esw1 = System(name="eSW", version_major=1, purpose="building firmware")
    koala_api.add_system(esw1)
    all_sdes = koala_api.get_all_systems()
    print(all_sdes)
    assert set(all_sdes) == set([esw1])


def test_add_two_sdes(koala_api):
    esw1 = System(name="eSW", version_major=1, purpose="building firmware")
    esw2 = System(name="eSW", version_major=2, purpose="building firmware")
    koala_api.add_system(esw1)
    koala_api.add_system(esw2)
    all_sdes = koala_api.get_all_systems()
    assert set(all_sdes) == set([esw1, esw2])


def test_get_all_tools_return_none_when_empty(koala_api):
    assert koala_api.get_all_tools() == []


def test_add_one_tool(koala_api):
    gcc = Tool(name="gcc", version_major=14, purpose="compiler")
    koala_api.add_tool(gcc)
    all_tools = koala_api.get_all_tools()
    assert set(all_tools) == set([gcc])


def test_add_two_tools(koala_api):
    gcc = Tool(name="gcc", version_major=14, purpose="compiler")
    clang = Tool(name="clang", version_major=12, purpose="compiler")
    koala_api.add_tool(gcc)
    koala_api.add_tool(clang)
    all_tools = koala_api.get_all_tools()
    assert set(all_tools) == set([gcc, clang])


def test_get_tool_for_system_when_empty(koala_api):
    esw1 = System(name="eSW", version_major=1, purpose="building firmware")
    tools = koala_api.get_tools_for_system(esw1)
    assert tools == []


def test_link_existing_tool_to_existing_sde(koala_api):
    esw1 = System(name="eSW", version_major=1, purpose="building firmware")
    koala_api.add_system(esw1)
    gcc = Tool(name="gcc", version_major=14, purpose="compiler")
    koala_api.add_tool(gcc)
    koala_api.link_tools_to_system(tools=[gcc], system=esw1)
    tools = koala_api.get_tools_for_system(esw1)
    assert set(tools) == set([gcc])


def test_submit_change_for_given_user_and_given_tool():
    pass


def test_submit_change_for_given_user_and_given_sde():
    pass


def test_user_approves_given_change():
    pass


def test_get_all_tools_from_give_side():
    pass


def test_get_all_tools_not_in_any_sde():
    pass


def test_get_all_sdes_relying_on_given_tool():
    pass


def test_get_all_gmp_relevant_tools():
    pass


def test_get_all_changes_for_given_tool():
    pass


def test_get_all_changes_for_given_tool_between_date1_and_date2():
    pass


def test_get_all_changes_for_given_sde_between_date1_and_date2():
    pass


def test_get_all_tools_owned_by_given_user():
    pass


def test_get_all_sdes_owned_by_given_user():
    pass


def test_get_all_documents_for_given_tool():
    pass


def test_get_all_documents_for_given_sde():
    pass


def test_get_status_for_given_tool():
    pass


def test_get_status_for_given_sde():
    pass


def test_get_number_of_days_left_before_next_periodic_review_for_given_tool():
    pass


def test_get_number_of_days_left_before_next_periodic_review_for_given_sde():
    pass
