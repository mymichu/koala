from typing import List

from koala.api.document import Document as DocumentApiModel
from koala.api.system import System as SystemApiModel
from koala.api.tool import Tool as ToolApiModel

from .types import DocumentExtended, SystemExtended, ToolExtended


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
