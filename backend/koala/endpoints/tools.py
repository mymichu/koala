from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from koala.api.document import DocumentApi
from koala.api.tool import Tool as ToolApiModel
from koala.api.tool import ToolApi
from koala.api.tool import ToolStatus as ToolStatusApi
from koala.api.types import Document as DocumentApiModel
from koala.endpoints.helper import converter
from koala.endpoints.helper.types import (
    Document,
    DocumentExtended,
    SystemExtended,
    Tool,
    ToolExtended,
)
from koala.factory import ContainerApi

router = APIRouter()


# pylint: disable=duplicate-code
class ToolStatus(BaseModel):
    is_productive: bool
    amount_documents_released: int
    amount_documents_unreleased: int
    amount_change_requests_closed: int
    amount_change_requests_open: int


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


@router.get("/tools/{identity}", tags=["tools"], response_model=ToolStatus)
@inject
async def get_system_status(
    identity: int, tool_api: ToolApi = Depends(Provide[ContainerApi.api_tool_factory])
) -> ToolStatus:
    tool_api_status_model: ToolStatusApi = tool_api.get_tool_status(identity)
    return ToolStatus(
        is_productive=tool_api_status_model.is_productive,
        amount_documents_released=tool_api_status_model.amount_documents_released,
        amount_documents_unreleased=tool_api_status_model.amount_documents_unreleased,
        amount_change_requests_closed=tool_api_status_model.amount_change_requests_closed,
        amount_change_requests_open=tool_api_status_model.amount_change_requests_open,
    )


@router.post("/tools/{identity}/documents", tags=["tools"], response_model=DocumentExtended)
@inject
async def add_create_document_to_tools(
    identity: int,
    document: Document,
    tool_api: ToolApi = Depends(Provide[ContainerApi.api_tool_factory]),
    document_api: DocumentApi = Depends(Provide[ContainerApi.api_document_factory]),
) -> DocumentExtended:
    document_database = document_api.add_document(DocumentApiModel(document.name, document.path))
    tool_api.add_tool_document(identity, document_database)
    return converter.convert_document(document_database)


@router.get("/tools/{identity}/documents", tags=["tools"], response_model=List[DocumentExtended])
@inject
async def get_system_documents(
    identity: int, tool_api: ToolApi = Depends(Provide[ContainerApi.api_tool_factory])
) -> List[DocumentExtended]:
    documents_api_model: List[DocumentApiModel] = tool_api.get_tool_documents(identity)
    return converter.convert_documents(documents_api_model)


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


@router.post("/tools/{identity}/owner", tags=["tools"])
@inject
async def add_tool_owner(
    identity: int, owner_identity: int, tool_api: ToolApi = Depends(Provide[ContainerApi.api_tool_factory])
) -> None:
    tool_api.add_tool_owner(identity, owner_identity)
