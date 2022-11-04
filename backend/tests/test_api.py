import pytest
from immudb import ImmudbClient


@pytest.fixture
def setup_test_database():
    URL = "url"
    USERNAME = "username"
    PASSWORD = "password"
    DATABASE = "pytest"
    client = ImmudbClient(URL)
    client.login(USERNAME, PASSWORD, DATABASE)
    client.createDatabase(DATABASE)
    yield client
    client.deleteDatabase(DATABASE)


def test_get_all_sdes_returns_none_when_empty(setup_test_database):
    client = setup_test_database()
    assert get_all_sdes(client) == []


def test_add_one_sde(setup_test_database):
    client = setup_test_database()
    esw1 = SDE(name="eSW", version="1.0", purpose="building firmware")
    add_sde(client, esw1)
    all_sdes = get_all_sdes(client)
    assert set(all_sdes) ==  set(esw1)


def test_add_two_sdes(setup_test_database):
    client = setup_test_database()
    esw1 = SDE(name="eSW", version="1.0", purpose="building firmware")
    esw2 = SDE(name="eSW", version="2.0", purpose="building firmware")
    add_sde(client, esw1)
    add_sde(client, esw2)
    all_sdes = get_all_sdes(client)
    assert set(all_sdes) == set([esw1, esw2])


def test_get_all_tools_return_none_when_emoty(setup_test_database):
    client = setup_test_database()
    assert get_all_tools(client) == None


def test_add_one_tool(setup_test_database):
    client = setup_test_database()
    gcc = Tool(name="gcc", version="14.0", purpose="compiler")
    add_tool(client, gcc)
    all_tools = get_all_tools(client)
    assert set(all_tools) == set([gcc])


def test_add_two_tools(setup_test_database):
    client = setup_test_database()
    gcc = Tool(name="gcc", version="14.0", purpose="compiler")
    clang = Tool(name="clang", version="12.0", purpose="compiler")
    add_tool(client, gcc)
    add_tool(client, clang)
    all_tools = get_all_tools(client)
    assert set(all_tools) == set([gcc, clang])
    

def test_link_existing_tool_to_existing_sde():
    pass

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

