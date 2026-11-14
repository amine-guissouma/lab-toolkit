from lab_toolkit.decorators.cli import handle_errors
from lab_toolkit.deployment.pipeline.apply_config import apply_config_pipeline
from lab_toolkit.deployment.pipeline.show_config import show_config_pipeline
from lab_toolkit.deployment.pipeline.validation_config import validate_pipeline


@handle_errors("Configuration de déploiement valide.")
def validate(args):
    """Vérifie la configuration de déploiement."""
    validate_pipeline()


@handle_errors("Aucune modification effectuée.")
def show_config(args):
    """Affiche la configuration de déploiement proposée."""
    show_config_pipeline()


@handle_errors("Configuration de déploiement mise à jour.")
def apply_config(args):
    """Calcule et enregistre la configuration de déploiement."""
    apply_config_pipeline()


def add_deployment_commands(subparsers):
    deployment_parser = subparsers.add_parser(
        "deployment",
        help="Gestion de la configuration de déploiement.",
    )

    deployment_subparsers = deployment_parser.add_subparsers(
        dest="deployment_command",
        required=True,
    )

    validate_parser = deployment_subparsers.add_parser(
        "validate",
        help="Vérifier la configuration de déploiement.",
    )
    validate_parser.set_defaults(func=validate)

    show_config_parser = deployment_subparsers.add_parser(
        "show_config",
        help="Afficher la configuration de déploiement proposée.",
    )
    show_config_parser.set_defaults(func=show_config)

    apply_config_parser = deployment_subparsers.add_parser(
        "apply_config",
        help="Appliquer la configuration de déploiement calculée.",
    )
    apply_config_parser.set_defaults(func=apply_config)
