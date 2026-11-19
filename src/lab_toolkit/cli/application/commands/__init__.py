from lab_toolkit.cli.application.commands.deployment import add_deployment_commands


def register_commands(subparsers):
    """Enregistre les commandes disponibles dans lab-toolkit."""

    add_deployment_commands(subparsers)
