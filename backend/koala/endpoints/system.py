from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from koala.api.document import DocumentApi
from koala.api.system import System as SystemApiModel
from koala.api.system import SystemApi
from koala.api.system import SystemStatus as SystemStatusApi
from koala.api.types import Document as DocumentApiModel
from koala.factory import ContainerApi

router = APIRouter()


class System(BaseModel):
    name: str
    version_major: int
    purpose: str


class SystemExtended(System):
    identity: int


class Document(BaseModel):
    name: str
    path: str


class DocumentExtended(Document):
    name: str
    path: str
    identity: int


# pylint: disable=duplicate-code
class SystemStatus(BaseModel):
    released_documents: int
    unreleased_documents: int
    released_tools: int
    unreleased_tools: int
    closed_change_requests: int
    open_change_requests: int


def convert_system(system_api: SystemApiModel) -> SystemExtended:
    return SystemExtended(
        name=system_api.name,
        version_major=system_api.version_major,
        purpose=system_api.purpose,
        identity=system_api.identity,
    )


def convert_systems(systems_api: List[SystemApiModel]) -> List[SystemExtended]:
    return [convert_system(system) for system in systems_api]


def convert_document(document: DocumentApiModel) -> DocumentExtended:
    return DocumentExtended(name=document.name, path=document.path, identity=document.identity)


def convert_documents(documents_api: List[DocumentApiModel]) -> List[DocumentExtended]:
    return [convert_document(document) for document in documents_api]


@router.get("/systems/", tags=["systems"], response_model=List[SystemExtended])
@inject
async def read_all_systems(
    system_api: SystemApi = Depends(Provide[ContainerApi.api_system_factory]),
) -> List[SystemExtended]:
    systems_api = system_api.get_all_systems()
    return convert_systems(systems_api)


@router.post("/systems/", tags=["systems"])
@inject
async def create_system(
    system: System, system_api: SystemApi = Depends(Provide[ContainerApi.api_system_factory])
) -> SystemExtended:
    system_api_model = system_api.add_system(SystemApiModel(system.name, system.version_major, system.purpose))
    return convert_system(system_api_model)


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
    return convert_documents(documents_api_model)


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
    return convert_document(document_database)
