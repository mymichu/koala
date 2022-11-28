from typing import List

from koala.api.change import Change as ChangeApiModel
from koala.api.document import Document as DocumentApiModel
from koala.api.system import System as SystemApiModel
from koala.api.tool import Tool as ToolApiModel
from koala.api.user import UserData as UserDataApi

from .types import (
    ChangeExtended,
    DocumentExtended,
    SystemExtended,
    ToolExtended,
    UserExtended,
)


def convert_tool(tool_api: ToolApiModel) -> ToolExtended:
    return ToolExtended(
        name=tool_api.name,
        version_major=tool_api.version_major,
        purpose=tool_api.purpose,
        identity=tool_api.identity,
        gmp_relevant=tool_api.gmp_relevant,
    )


def convert_tools(tool_api: List[ToolApiModel]) -> List[ToolExtended]:
    return [convert_tool(tool) for tool in tool_api]


def convert_change(change_api: ChangeApiModel) -> ChangeExtended:
    return ChangeExtended(
        entity_id=change_api.entity_id,
        requester_id=change_api.requester_id,
        reviewer_id=change_api.reviewer_id,
        description=change_api.description,
        identity=change_api.identity,
    )


def convert_changes(change_api: List[ChangeApiModel]) -> List[ChangeExtended]:
    return [convert_change(change) for change in change_api]


def convert_system(system_api: SystemApiModel) -> SystemExtended:
    return SystemExtended(
        name=system_api.name,
        version_major=system_api.version_major,
        purpose=system_api.purpose,
        identity=system_api.identity,
    )


def convert_user(user_data_api: UserDataApi) -> UserExtended:
    return UserExtended(
        name=user_data_api.name,
        first_name=user_data_api.first_name,
        email=user_data_api.email,
        active=user_data_api.active,
        identity=user_data_api.identity,
    )


def convert_systems(systems_api: List[SystemApiModel]) -> List[SystemExtended]:
    return [convert_system(system) for system in systems_api]


def convert_document(document: DocumentApiModel) -> DocumentExtended:
    return DocumentExtended(name=document.name, path=document.path, identity=document.identity)


def convert_documents(documents_api: List[DocumentApiModel]) -> List[DocumentExtended]:
    return [convert_document(document) for document in documents_api]


def convert_users(users: List[UserDataApi]) -> List[UserExtended]:
    return [convert_user(user) for user in users]
