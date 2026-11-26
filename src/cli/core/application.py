import argparse

from cli.core.metadata import get_project_metadata


def run_cli(
    distribution_name: str,
    register_commands,
    argv=None,
):
    """
    Construit et exécute une interface CLI.

    Args:
        distribution_name: Nom de la distribution installée.
        register_commands: Fonction qui enregistre les commandes CLI.
        argv: Arguments à analyser. Si None, utilise sys.argv.
    """

    project = get_project_metadata(distribution_name)

    parser = argparse.ArgumentParser(
        prog=project["name"],
        description=project["description"],
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"{project['name']} {project['version']}",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    register_commands(subparsers)

    args = parser.parse_args(argv)

    return args.func(args)
