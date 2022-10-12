import argparse

from .container import Container


def main() -> None:
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--dummy",
        action="store_true",
        help="Enable dummy mode helps for system test or development",
        required=False,
        default=False,
    )

    args = parser.parse_args()

    container = Container()
    container.config.dummy.override(args.dummy)
    container.init_resources()
    container.wire(modules=[__name__])
    # TODO


if __name__ == "__main__":
    main()
