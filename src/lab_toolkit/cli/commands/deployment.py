
from lab_toolkit.decorators.cli import handle_errors
from lab_toolkit.deployment.pipeline_validation import validate_pipeline


@handle_errors("Configuration de déploiement valide.")
def validate(args):
    """Vérifie la configuration de déploiement."""

    validate_pipeline()


def configure(args):
    print("Configuration du déploiement : fonctionnalité à développer.")


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

    configure_parser = deployment_subparsers.add_parser(
        "configure",
        help="Préparer la configuration de déploiement.",
    )
    configure_parser.set_defaults(func=configure)
