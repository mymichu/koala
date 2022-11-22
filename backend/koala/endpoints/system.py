from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from koala.api.document import Document as DocumentApi
from koala.api.system import System as SystemApiModel
from koala.api.system import SystemApi
from koala.api.system import SystemStatus as SystemStatusApi
from koala.api.types import Document
from koala.factory import ContainerApi

router = APIRouter()


class System(BaseModel):
    name: str
    version_major: int
    purpose: str


class SystemExtended(System):
    identity: int


class Documents(BaseModel):
    name: str
    path: str


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


def convert_documents(documents_api: List[DocumentApi]) -> List[Document]:
    documents = map(
        lambda system: Document(name=system.name, path=system.path),
        documents_api,
    )
    return list(documents)


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
) -> List[Document]:
    system_api_model: SystemStatusApi = system_api.get_system_status(identity)
    return SystemStatus(
        released_documents=system_api_model.released_documents,
        unreleased_documents=system_api_model.unreleased_documents,
        released_tools=system_api_model.released_tools,
        unreleased_tools=system_api_model.unreleased_tools,
        closed_change_requests=system_api_model.closed_change_requests,
        open_change_requests=system_api_model.open_change_requests,
    )


@router.get("/systems/{identity}/documents", tags=["systems"], response_model=List[Document])
@inject
async def get_system_documents(
    identity: int, system_api: SystemApi = Depends(Provide[ContainerApi.api_system_factory])
) -> List[Document]:
    documents_api_model = system_api.get_system_documents(identity)
    return convert_documents(documents_api_model)
