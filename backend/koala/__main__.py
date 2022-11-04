from pydoc import cli
from dependency_injector.wiring import Provide, inject
from koala.database.types import ToolId
from immudb import ImmudbClient
from dependency_injector import providers

from koala.container import Container
from koala.database.tool import Tool, System


@inject
def run(client: ImmudbClient = Provide[Container.client]) -> None:
   pass
   #client.login("immudb", "immudb", database="defaultdb")
   #gcc_compiler = Tool(client, ToolId("GCC", 9))
   #gcc_compiler.add_to_database("COMPILE FOR ARM")
   #clang_compiler = Tool(client, ToolId("clang", 10))
   #clang_compiler.add_to_database("COMPILE FOR X64")
   #system = System(client, "SYS1", 1)
   #system.add("System for embedded")
   #system.link_to_tool(gcc_compiler.tool_id)
   #system.link_to_tool(clang_compiler.tool_id)
   #print("--- all tool depend on SYS1 ---")
   #print(system.get_linked_tools())
   #print("--- all tool depend on GCC ---")
   #print(gcc_compiler.get_linked_systems())


def main() -> None:
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    run()
    # TODO


if __name__ == "__main__":
    main()
