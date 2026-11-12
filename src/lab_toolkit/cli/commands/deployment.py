from lab_toolkit.decorators.cli import handle_errors
from lab_toolkit.deployment.config import load_config, save_config
from lab_toolkit.deployment.configuration import build_deployment_config
from lab_toolkit.deployment.pipeline_validation import validate_pipeline
from lab_toolkit.exceptions import LabToolkitError


@handle_errors("Configuration de déploiement valide.")
def validate(args):
    """Vérifie la configuration de déploiement."""
    validate_pipeline()


def show_config(args):
    """Affiche la configuration de déploiement proposée."""
    try:
        current_config = load_config()

        new_config = {
            **current_config,
            **build_deployment_config(),
        }

        print("Configuration actuelle :")
        print(f"  remoteDir : {current_config['remoteDir']}")
        print(f"  base      : {current_config['base']}")

        print("\nConfiguration proposée :")
        print(f"  remoteDir : {new_config['remoteDir']}")
        print(f"  base      : {new_config['base']}")

        print("\nAucune modification effectuée.")
        return 0

    except LabToolkitError as error:
        print(f"ERREUR : {error}")
        return 1


def apply_config(args):
    """Calcule et enregistre la configuration de déploiement."""
    try:
        current_config = load_config()

        new_config = {
            **current_config,
            **build_deployment_config(),
        }

        save_config(new_config)

        print("Configuration de déploiement mise à jour.")
        print(f"  remoteDir : {new_config['remoteDir']}")
        print(f"  base      : {new_config['base']}")

        return 0

    except LabToolkitError as error:
        print(f"ERREUR : {error}")
        return 1


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
