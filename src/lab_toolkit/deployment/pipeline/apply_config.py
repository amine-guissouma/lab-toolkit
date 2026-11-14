from lab_toolkit.deployment.config import load_config, save_config
from lab_toolkit.deployment.configuration import build_deployment_config
from lab_toolkit.deployment.constants import DEPLOYMENT


def apply_config_pipeline() -> None:
    """Calcule et enregistre la configuration de déploiement."""
    current_config = load_config()

    new_config = {
        **current_config,
        **build_deployment_config(),
    }

    save_config(new_config)

    print(f"  {DEPLOYMENT.REMOTE_DIR} : {new_config[DEPLOYMENT.REMOTE_DIR]}")
    print(f"  {DEPLOYMENT.BASE}      : {new_config[DEPLOYMENT.BASE]}")
