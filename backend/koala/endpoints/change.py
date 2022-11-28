from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from koala.api.change import Change as ChangeApiModel
from koala.api.change import ChangeApi
from koala.endpoints.helper import converter
from koala.endpoints.helper.types import Change, ChangeExtended
from koala.factory import ContainerApi

router = APIRouter()


@router.post("/change/", tags=["change"], response_model=ChangeExtended)
@inject
async def create_change(
    change: Change, change_api: ChangeApi = Depends(Provide[ContainerApi.api_change_factory])
) -> ChangeExtended:
    change_api_model = change_api.add_change(
        ChangeApiModel(
            entity_id=change.entity_id, requester_id=change.requester_id, reviewer_id=-1, description=change.description
        )
    )
    return converter.convert_change(change_api_model)


@router.get("/change/", tags=["change"], response_model=List[ChangeExtended])
@inject
async def read_all_changes(
    change_api: ChangeApi = Depends(Provide[ContainerApi.api_change_factory]),
) -> List[ChangeExtended]:
    changes = change_api.get_all_changes()
    return converter.convert_changes(changes)


@router.get("/change/open", tags=["change"], response_model=List[ChangeExtended])
@inject
async def read_all_open_changes(
    change_api: ChangeApi = Depends(Provide[ContainerApi.api_change_factory]),
) -> List[ChangeExtended]:
    changes = change_api.get_all_changes_open()
    return converter.convert_changes(changes)


@router.put("/change/{identity}/reviewer", tags=["change"])
@inject
async def update_state(
    identity: int, reviewer_id: int, change_api: ChangeApi = Depends(Provide[ContainerApi.api_change_factory])
) -> None:
    change_api.update_reviewer(identity, reviewer_id)
