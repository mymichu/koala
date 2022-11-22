from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from koala.api.document import Document as DocumentApi
from koala.api.system import System as SystemApiModel
from koala.api.system import SystemApi
from koala.api.types import Document
from koala.factory import ContainerApi

router = APIRouter()


class System(BaseModel):
    name: str
    version_major: int
    purpose: str


class SystemExtended(BaseModel):
    name: str
    version_major: int
    purpose: str
    identity: int


class Documents(BaseModel):
    name: str
    path: str


def convert_system(system_api: SystemApiModel) -> SystemExtended:
    return SystemExtended(
        name=system_api.name,
        version_major=system_api.version_major,
        purpose=system_api.purpose,
        identity=system_api.identity,
    )


def convert_systems(systems_api: List[SystemApiModel]) -> List[SystemExtended]:
    systems: List[SystemExtended] = []
    for system in systems_api:
        systems.append(convert_system(system))
    return systems


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


@router.get("/systems/{identity}/documents", tags=["systems"], response_model=List[Document])
@inject
async def get_system_documents(
    identity: int, system_api: SystemApi = Depends(Provide[ContainerApi.api_system_factory])
) -> List[Document]:
    documents_api_model = system_api.get_system_documents(identity)
    return convert_documents(documents_api_model)
