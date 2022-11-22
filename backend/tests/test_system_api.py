import pytest

from koala.api.document import DocumentApi
from koala.api.system import SystemApi, SystemStatus
from koala.api.tool import ToolApi
from koala.api.types import Document, System, Tool


@pytest.mark.usefixtures("koala_api")
def test_get_all_sdes_returns_none_when_empty(koala_api):
    api: SystemApi = koala_api.api_system_factory()
    assert api.get_all_systems() == []


def test_add_one_sde(koala_api):
    api: SystemApi = koala_api.api_system_factory()
    esw1 = System(name="eSW", version_major=1, purpose="building firmware")
    api.add_system(esw1)
    all_sdes = api.get_all_systems()
    print(all_sdes)
    assert set(all_sdes) == set([esw1])


def test_add_two_sdes_same_name_and_purpose_different_versions(koala_api):
    api: SystemApi = koala_api.api_system_factory()
    esw1 = System(name="eSW", version_major=1, purpose="building firmware")
    api.add_system(esw1)

    esw2 = System(name="eSW", version_major=2, purpose="building firmware")
    api.add_system(esw2)

    all_sdes = api.get_all_systems()
    assert set(all_sdes) == set([esw1, esw2])


def test_link_existing_sde_to_existing_tool(koala_api):
    api_tool: ToolApi = koala_api.api_tool_factory()
    api_system: SystemApi = koala_api.api_system_factory()
    esw1 = System(name="eSW", version_major=1, purpose="building firmware")
    api_system.add_system(esw1)

    project_x = System(name="project x", version_major=1, purpose="building firmware for project X")
    api_system.add_system(project_x)

    project_y = System(name="project y", version_major=2, purpose="building firmware for project Y")
    api_system.add_system(project_y)

    gcc = Tool(name="gcc", version_major=14, purpose="compiler")
    api_tool.add_tool(gcc)

    api_tool.link_tools_to_system(tools=[gcc], system=esw1)
    api_tool.link_tools_to_system(tools=[gcc], system=project_x)

    systems = api_system.get_systems_for_tool(gcc)
    assert set(systems) == set([esw1, project_x])


def test_get_all_documents_for_given_sde(koala_api):
    api_system: SystemApi = koala_api.api_system_factory()
    api_document: DocumentApi = koala_api.api_document_factory()
    esw1 = System(name="esw1", version_major=13, purpose="esw1")
    doc_a = Document(name="intro", path="path/to/intro")
    doc_b = Document(name="class", path="path/to/class")

    api_document.add_document(doc_a)
    api_document.add_document(doc_b)

    esw1_database = api_system.add_system(esw1)
    api_system.add_system_document(esw1, doc_a)
    api_system.add_system_document(esw1, doc_b)

    result = api_system.get_system_documents(esw1_database.identity)
    assert set(result) == set(
        [Document(name="intro", path="path/to/intro"), Document(name="class", path="path/to/class")]
    )


@pytest.mark.skip(reason="Not Implemented")
def test_get_all_sdes_owned_by_given_user():
    pass


@pytest.mark.skip(reason="Not Implemented")
def test_submit_change_for_given_user_and_given_sde():
    pass


def test_get_status_for_given_sde_released_documents(koala_api):
    api_system: SystemApi = koala_api.api_system_factory()
    api_document: DocumentApi = koala_api.api_document_factory()
    esw1 = System(name="esw1", version_major=13, purpose="esw1")
    doc_a = Document(name="intro", path="path/to/intro")
    doc_b = Document(name="class", path="path/to/class")

    esw1_db = api_system.add_system(esw1)
    doc_a_db = api_document.add_document(doc_a)
    doc_b_db = api_document.add_document(doc_b)
    api_system.add_system_document(esw1_db, doc_a)
    api_system.add_system_document(esw1_db, doc_b)
    api_document.update_release_status(doc_a_db.identity, True)
    api_document.update_release_status(doc_b_db.identity, True)
    api_document.update_release_status(doc_a_db.identity, False)

    result = api_system.get_system_status(esw1_db.identity)

    assert SystemStatus(1, 1, 0, 0, 0, 0) == result


@pytest.mark.skip(reason="Not Implemented")
def test_get_all_changes_for_given_sde_between_date1_and_date2():
    pass


@pytest.mark.skip(reason="Not Implemented")
def test_get_number_of_days_left_before_next_periodic_review_for_given_sde():
    pass
