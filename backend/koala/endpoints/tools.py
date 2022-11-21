import json
from typing import Dict

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from koala.api.tool import ToolApi
from koala.factory import ContainerApi

router = APIRouter()


@router.get("/tools/", tags=["tools"])
@inject
async def read_all_tools(tool_api: ToolApi = Depends(Provide[ContainerApi.api_tool_factory])) -> str:
    tools = tool_api.get_all_tools()
    return json.dumps(tools)


@router.get("/users/me", tags=["users"])
async def read_user_me() -> Dict[str, str]:
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str) -> Dict[str, str]:
    return {"username": username}
