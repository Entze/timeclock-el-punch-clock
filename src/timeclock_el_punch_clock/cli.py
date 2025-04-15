import argparse
import pathlib
from typing import Sequence


def main(args: Sequence[str] | None = None) -> None:
    parser = create_argument_parser()
    parser.parse_args(args=args)


def execute_in(namespace: argparse.Namespace) -> None:
    pass


def create_argument_parser() -> argparse.ArgumentParser:
    ttlpc_parser = argparse.ArgumentParser()

    ttlpc_parser.add_argument("--file", "-f", type=pathlib.Path)

    ttlpc_commands_parser = ttlpc_parser.add_subparsers(title="commands")

    ttlpc_in_parser = ttlpc_commands_parser.add_parser("in")

    ttlpc_in_parser.set_defaults(func=execute_in)

    return ttlpc_parser
