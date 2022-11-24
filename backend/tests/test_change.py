import pytest

from koala.api.change import ChangeApi
from koala.api.system import SystemApi
from koala.api.tool import ToolApi
from koala.api.types import Change, System, Tool
from koala.api.user import UserApi, UserData


@pytest.mark.usefixtures("koala_api")
def test_create_system_change(koala_api):
    esw1: System = System(name="eSW", version_major=1, purpose="building firmware")
    api_sys: SystemApi = koala_api.api_system_factory()
    esw1 = api_sys.add_system(esw1)

    api_user: UserApi = koala_api.api_user_factory()
    api_user = api_user.add_user(UserData(name="muster", first_name="max", email="max.muster@email.com"))

    change: Change = Change(esw1.identity, api_user.identity, -1, "version increment")
    api_change: ChangeApi = koala_api.api_change_factory()
    change = api_change.add_change(change)

    changes = api_change.get_all_changes()

    assert len(changes) == 1
    assert change == changes[0]


@pytest.mark.usefixtures("koala_api")
def test_update_change(koala_api):
    api_tool: ToolApi = koala_api.api_tool_factory()
    gcc = Tool(name="gcc", version_major=14, purpose="compiler")
    api_tool.add_tool(gcc)

    api_user: UserApi = koala_api.api_user_factory()
    api_user = api_user.add_user(UserData(name="muster", first_name="max", email="max.muster@email.com"))

    change: Change = Change(gcc.identity, api_user.identity, -1, "version increment")
    api_change: ChangeApi = koala_api.api_change_factory()
    change = api_change.add_change(change)

    changes = api_change.get_all_changes()

    assert len(changes) == 1
    assert change == changes[0]


@pytest.mark.usefixtures("koala_api")
@pytest.mark.skip(reason="Not Implemented")
def test_user_approves_given_change(koala_api):
    pass


@pytest.mark.usefixtures("koala_api")
@pytest.mark.skip(reason="Not Implemented")
def test_user_refuses_given_change(koala_api):
    pass
