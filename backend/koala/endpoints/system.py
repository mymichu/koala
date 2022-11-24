from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from koala.api.document import DocumentApi
from koala.api.system import System as SystemApiModel
from koala.api.system import SystemApi
from koala.api.system import SystemStatus as SystemStatusApi
from koala.api.types import Document as DocumentApiModel
from koala.endpoints.helper import converter
from koala.endpoints.helper.types import (
    Document,
    DocumentExtended,
    System,
    SystemExtended,
    ToolExtended,
)
from koala.factory import ContainerApi

router = APIRouter()


# pylint: disable=duplicate-code
class SystemStatus(BaseModel):
    released_documents: int
    unreleased_documents: int
    released_tools: int
    unreleased_tools: int
    closed_change_requests: int
    open_change_requests: int


@router.get("/systems/", tags=["systems"], response_model=List[SystemExtended])
@inject
async def read_all_systems(
    system_api: SystemApi = Depends(Provide[ContainerApi.api_system_factory]),
) -> List[SystemExtended]:
    systems_api = system_api.get_all_systems()
    return converter.convert_systems(systems_api)


@router.post("/systems/", tags=["systems"])
@inject
async def create_system(
    system: System, system_api: SystemApi = Depends(Provide[ContainerApi.api_system_factory])
) -> SystemExtended:
    system_api_model = system_api.add_system(SystemApiModel(system.name, system.version_major, system.purpose))
    return converter.convert_system(system_api_model)


@router.get("/systems/{identity}", tags=["systems"], response_model=SystemStatus)
@inject
async def get_system_status(
    identity: int, system_api: SystemApi = Depends(Provide[ContainerApi.api_system_factory])
) -> SystemStatus:
    system_api_model: SystemStatusApi = system_api.get_system_status(identity)
    return SystemStatus(
        released_documents=system_api_model.released_documents,
        unreleased_documents=system_api_model.unreleased_documents,
        released_tools=system_api_model.released_tools,
        unreleased_tools=system_api_model.unreleased_tools,
        closed_change_requests=system_api_model.closed_change_requests,
        open_change_requests=system_api_model.open_change_requests,
    )


@router.get("/systems/{identity}/documents", tags=["systems"], response_model=List[DocumentExtended])
@inject
async def get_system_documents(
    identity: int, system_api: SystemApi = Depends(Provide[ContainerApi.api_system_factory])
) -> List[DocumentExtended]:
    documents_api_model = system_api.get_system_documents(identity)
    return converter.convert_documents(documents_api_model)


@router.get("/systems/{identity}/tools", tags=["systems"], response_model=List[ToolExtended])
@inject
async def get_system_tools(
    identity: int, system_api: SystemApi = Depends(Provide[ContainerApi.api_system_factory])
) -> List[ToolExtended]:
    tools_api_model = system_api.get_tools_for_system(identity)
    return converter.convert_tools(tools_api_model)


@router.post("/systems/{identity}/documents", tags=["systems"], response_model=DocumentExtended)
@inject
async def add_create_document_to_system(
    identity: int,
    document: Document,
    system_api: SystemApi = Depends(Provide[ContainerApi.api_system_factory]),
    document_api: DocumentApi = Depends(Provide[ContainerApi.api_document_factory]),
) -> DocumentExtended:
    document_database = document_api.add_document(DocumentApiModel(document.name, document.path))
    system_api.add_system_document(identity, document_database)
    return converter.convert_document(document_database)
