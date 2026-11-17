from lab_toolkit.deployment.config import load_config, save_config
from lab_toolkit.deployment.configuration import build_deployment_config
from lab_toolkit.deployment.constants import DEPLOYMENT
from lab_toolkit.deployment.git import get_current_branch


def apply_config_pipeline():
    """Calcule et enregistre la configuration de déploiement."""
    branch = get_current_branch()
    current_config = load_config()

    new_config = {
        **current_config,
        **build_deployment_config(),
    }

    save_config(new_config)

    return {
        "branch": branch,
        DEPLOYMENT.REMOTE_DIR: new_config[DEPLOYMENT.REMOTE_DIR],
        DEPLOYMENT.BASE: new_config[DEPLOYMENT.BASE],
    }
