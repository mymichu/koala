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
    is_productive: bool
    amount_documents_released: int
    amount_documents_unreleased: int
    amount_tools_productive: int
    amount_tools_not_productive: int
    amount_systems_productive: int
    amount_systems_not_productive: int
    amount_change_requests_closed: int
    amount_change_requests_open: int


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
        is_productive=system_api_model.is_productive,
        amount_documents_released=system_api_model.amount_documents_released,
        amount_documents_unreleased=system_api_model.amount_documents_unreleased,
        amount_tools_productive=system_api_model.amount_tools_productive,
        amount_tools_not_productive=system_api_model.amount_tools_not_productive,
        amount_systems_productive=system_api_model.amount_systems_productive,
        amount_systems_not_productive=system_api_model.amount_systems_not_productive,
        amount_change_requests_closed=system_api_model.amount_change_request_closed,
        amount_change_requests_open=system_api_model.amount_change_request_open,
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


@router.post("/systems/{identity}/owner", tags=["systems"])
@inject
async def add_system_owner(
    identity: int, owner_identity: int, system_api: SystemApi = Depends(Provide[ContainerApi.api_system_factory])
) -> None:
    system_api.add_system_owner(identity, owner_identity)
