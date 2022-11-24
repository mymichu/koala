from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from koala.api.tool import Tool as ToolApiModel
from koala.api.tool import ToolApi
from koala.endpoints.helper import converter
from koala.endpoints.helper.types import SystemExtended, Tool, ToolExtended
from koala.factory import ContainerApi

router = APIRouter()


@router.get("/tools/", tags=["tools"], response_model=List[ToolExtended])
@inject
async def read_all_tools(tool_api: ToolApi = Depends(Provide[ContainerApi.api_tool_factory])) -> List[ToolExtended]:
    tools = tool_api.get_all_tools()
    return converter.convert_tools(tools)


@router.post("/tools/", tags=["tools"], response_model=ToolExtended)
@inject
async def add_tool(tool: Tool, tool_api: ToolApi = Depends(Provide[ContainerApi.api_tool_factory])) -> ToolExtended:
    tool_api_model = tool_api.add_tool(
        ToolApiModel(tool.name, tool.version_major, tool.purpose, gmp_relevant=tool.gmp_relevant)
    )
    return converter.convert_tool(tool_api_model)


@router.post("/tools/{identity}/systems", tags=["tools"])
@inject
async def create_link_tool_to_system(
    identity: int, system_identity: int, tool_api: ToolApi = Depends(Provide[ContainerApi.api_tool_factory])
) -> None:
    tool_api.link_tools_to_system([identity], system_identity)


@router.get("/tools/{identity}/systems", tags=["tools"], response_model=List[SystemExtended])
@inject
async def get_system_tools(
    identity: int, tool_api: ToolApi = Depends(Provide[ContainerApi.api_tool_factory])
) -> List[SystemExtended]:
    system_api_models = tool_api.get_systems_for_tool(identity)
    return converter.convert_systems(system_api_models)
