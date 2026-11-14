from lab_toolkit.deployment.config import load_config
from lab_toolkit.deployment.configuration import build_deployment_config
from lab_toolkit.deployment.constants import DEPLOYMENT


def show_config_pipeline() -> None:
    """Affiche la configuration de déploiement proposée."""
    current_config = load_config()

    new_config = {
        **current_config,
        **build_deployment_config(),
    }

    print("Configuration actuelle :")
    print(f"  {DEPLOYMENT.REMOTE_DIR}  : {current_config[DEPLOYMENT.REMOTE_DIR]}")
    print(f"  {DEPLOYMENT.BASE}      : {current_config[DEPLOYMENT.BASE]}")

    print("\nConfiguration proposée :")
    print(f"  {DEPLOYMENT.REMOTE_DIR} : {new_config[DEPLOYMENT.REMOTE_DIR]}")
    print(f"  {DEPLOYMENT.BASE}      : {new_config[DEPLOYMENT.BASE]}")

    print("\nAucune modification effectuée.")
