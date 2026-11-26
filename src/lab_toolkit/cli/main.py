import sys

from cli.core.application import run_cli
from lab_toolkit.cli.application.commands import register_commands
from lab_toolkit.cli.application.config import DISTRIBUTION_NAME


def main():
    return run_cli(
        distribution_name=DISTRIBUTION_NAME,
        register_commands=register_commands,
    )


if __name__ == "__main__":
    sys.exit(main())
