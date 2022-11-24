from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from koala.api.tool import Tool as ToolApiModel
from koala.api.tool import ToolApi
from koala.endpoints.types import Tool, ToolExtended
from koala.factory import ContainerApi

router = APIRouter()


def convert_tool(tool_api: ToolApiModel) -> ToolExtended:
    return ToolExtended(
        name=tool_api.name,
        version_major=tool_api.version_major,
        purpose=tool_api.purpose,
        identity=tool_api.identity,
        gmp_relevant=tool_api.gmp_relevant,
    )


def convert_tools(tool_api: List[ToolApiModel]) -> List[ToolExtended]:
    return [convert_tool(tool) for tool in tool_api]


@router.get("/tools/", tags=["tools"], response_model=List[ToolExtended])
@inject
async def read_all_tools(tool_api: ToolApi = Depends(Provide[ContainerApi.api_tool_factory])) -> List[ToolExtended]:
    tools = tool_api.get_all_tools()
    return convert_tools(tools)


@router.post("/tools/", tags=["tools"], response_model=ToolExtended)
@inject
async def add_tool(tool: Tool, tool_api: ToolApi = Depends(Provide[ContainerApi.api_tool_factory])) -> ToolExtended:
    tool_api_model = tool_api.add_tool(
        ToolApiModel(tool.name, tool.version_major, tool.purpose, gmp_relevant=tool.gmp_relevant)
    )
    return convert_tool(tool_api_model)
