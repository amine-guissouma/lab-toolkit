
import argparse

from lab_toolkit.cli.commands.deployment import add_deployment_commands


def main():
    parser = argparse.ArgumentParser(
        prog="lab-toolkit",
        description="Outils communs de développement des laboratoires.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="lab-toolkit 0.1.0",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    add_deployment_commands(subparsers)

    args = parser.parse_args()
    return args.func(args)