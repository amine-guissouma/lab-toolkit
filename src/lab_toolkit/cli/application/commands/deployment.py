from lab_toolkit.cli.application.arguments.logger import add_display_arguments
from lab_toolkit.cli.application.decorators.command import cli_command
from lab_toolkit.deployment.pipeline.apply_config import apply_config_pipeline
from lab_toolkit.deployment.pipeline.init_config import init_config_pipeline
from lab_toolkit.deployment.pipeline.show_config import show_config_pipeline
from lab_toolkit.deployment.pipeline.validation_config import validate_pipeline


@cli_command(action="validate", target="deployment.json")
def validate(args):
    """Vérifie la configuration de déploiement."""
    return validate_pipeline()


@cli_command(action="show", target="deployment.json")
def show_config(args):
    """Affiche la configuration de déploiement proposée."""
    return show_config_pipeline()


@cli_command(action="update", target="deployment.json")
def apply_config(args):
    """Calcule et enregistre la configuration de déploiement."""
    return apply_config_pipeline()


@cli_command(action="init", target="deployment.json")
def init(args):
    """Initialise les fichiers de configuration de déploiement."""
    return init_config_pipeline()


def add_deployment_commands(subparsers):

    deployment_parser = subparsers.add_parser(
        "deployment",
        help="Gestion de la configuration de déploiement.",
    )

    deployment_subparsers = deployment_parser.add_subparsers(
        dest="deployment_command",
        required=True,
    )

    init_parser = deployment_subparsers.add_parser(
        init.__name__,
        help="Initialiser les fichiers de configuration de déploiement.",
    )
    init_parser.set_defaults(func=init)
    add_display_arguments(init_parser)

    validate_parser = deployment_subparsers.add_parser(
        validate.__name__,
        help="Vérifier la configuration de déploiement.",
    )
    validate_parser.set_defaults(func=validate)
    add_display_arguments(validate_parser)

    show_config_parser = deployment_subparsers.add_parser(
        show_config.__name__,
        help="Afficher la configuration de déploiement proposée.",
    )
    show_config_parser.set_defaults(func=show_config)
    add_display_arguments(show_config_parser)

    apply_config_parser = deployment_subparsers.add_parser(
        apply_config.__name__,
        help="Appliquer la configuration de déploiement calculée.",
    )
    apply_config_parser.set_defaults(func=apply_config)
    add_display_arguments(apply_config_parser)
