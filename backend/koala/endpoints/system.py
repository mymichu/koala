from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from koala.api.system import System as SystemApiModel
from koala.api.system import SystemApi
from koala.factory import ContainerApi

router = APIRouter()


class System(BaseModel):
    name: str
    version_major: int
    purpose: str


@router.get("/systems/", tags=["systems"], response_model=List[System])
@inject
async def read_all_systems(system_api: SystemApi = Depends(Provide[ContainerApi.api_system_factory])) -> List[System]:
    systems_api = system_api.get_all_systems()
    systems = map(
        lambda system: System(name=system.name, version_major=system.version_major, purpose=system.purpose), systems_api
    )
    return list(systems)


@router.post("/systems/", tags=["systems"])
@inject
async def create_system(
    system: System, system_api: SystemApi = Depends(Provide[ContainerApi.api_system_factory])
) -> System:
    system_api.add_system(SystemApiModel(system.name, system.version_major, system.purpose))
    return system
