from lab_toolkit.decorators.cli import handle_errors
from lab_toolkit.deployment.config import load_config, save_config
from lab_toolkit.deployment.configuration import build_deployment_config
from lab_toolkit.deployment.pipeline_validation import validate_pipeline
from lab_toolkit.exceptions import LabToolkitError


@handle_errors("Configuration de déploiement valide.")
def validate(args):
    """Vérifie la configuration de déploiement."""

    validate_pipeline()


def configure(args):
    """Prépare ou applique la configuration de déploiement."""

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

        if not args.apply:
            print("\nAucune modification effectuée. Utilisez --apply pour enregistrer.")
            return 0

        save_config(new_config)

        print("\nConfiguration de déploiement mise à jour.")
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

    configure_parser = deployment_subparsers.add_parser(
        "configure",
        help="Préparer la configuration de déploiement.",
    )

    configure_parser.add_argument(
        "--apply",
        action="store_true",
        help="Enregistrer la configuration proposée.",
    )

    configure_parser.set_defaults(func=configure)
