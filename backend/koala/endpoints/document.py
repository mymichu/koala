from enum import Enum

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from koala.api.document import DocumentApi
from koala.factory import ContainerApi

router = APIRouter()


# pylint: disable=invalid-name
class State(str, Enum):
    relased = "relased"
    obsolete = "obsolete"
    in_progress = "in_progress"


@router.put("/documents/{identity}/state", tags=["documets"])
@inject
async def update_state(
    identity: int, state: State, document_api: DocumentApi = Depends(Provide[ContainerApi.api_document_factory])
) -> None:

    if state == State.relased:
        document_api.update_release_status(identity, True)
    else:
        document_api.update_release_status(identity, False)

    # TODO: implement other states
