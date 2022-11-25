from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from koala.api.system import System as SystemApiModel
from koala.api.system import SystemApi
from koala.api.tool import Tool as ToolApiModel
from koala.api.tool import ToolApi
from koala.api.user import UserApi
from koala.api.user import UserData as UserDataApi
from koala.endpoints.helper import converter
from koala.endpoints.helper.types import Ownership, User, UserExtended
from koala.factory import ContainerApi

router = APIRouter()


@router.post("/user/", tags=["user"])
@inject
async def create_user(user: User, user_api: UserApi = Depends(Provide[ContainerApi.api_user_factory])) -> UserExtended:
    user_api_model = user_api.add_user(UserDataApi(name=user.name, first_name=user.first_name, email=user.email))
    return converter.convert_user(user_api_model)


@router.get("/user/{identity}", tags=["user"], response_model=UserExtended)
@inject
async def get_tools_owned_by(
    identity: int,
    user_api: UserApi = Depends(Provide[ContainerApi.api_user_factory]),
    tool_api: ToolApi = Depends(Provide[ContainerApi.api_tool_factory]),
    system_api: SystemApi = Depends(Provide[ContainerApi.api_system_factory]),
) -> UserExtended:
    user_details_api = user_api.get_user_details(identity)
    user_details = converter.convert_user(user_details_api)
    tool_api_model: List[ToolApiModel] = tool_api.get_all_tools_owned_by(identity)
    owned_tools = converter.convert_tools(tool_api_model)
    system_api_model: List[SystemApiModel] = system_api.get_all_system_owned_by(identity)
    owned_systems = converter.convert_systems(system_api_model)
    user_details.ownership = Ownership(systems=owned_systems, tools=owned_tools)
    return user_details
