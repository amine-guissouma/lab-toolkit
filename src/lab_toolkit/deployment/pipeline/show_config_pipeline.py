from lab_toolkit.deployment.config import load_config
from lab_toolkit.deployment.configuration import build_deployment_config


def show_config_pipeline() -> None:
    """Affiche la configuration de déploiement proposée."""
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
