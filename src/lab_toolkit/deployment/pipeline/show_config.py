from lab_toolkit.deployment.config import load_config
from lab_toolkit.deployment.configuration import build_deployment_config
from lab_toolkit.deployment.constants import DEPLOYMENT
from lab_toolkit.deployment.git import get_current_branch


def show_config_pipeline():
    """Affiche la configuration de déploiement proposée."""
    branch = get_current_branch()
    current_config = load_config()
    proposed_config = build_deployment_config()

    return {
        "Branche": branch,
        "remoteDir actuel": current_config.get(DEPLOYMENT.REMOTE_DIR),
        "base actuel": current_config.get(DEPLOYMENT.BASE),
        "remoteDir proposé": proposed_config.get(DEPLOYMENT.REMOTE_DIR),
        "base proposé": proposed_config.get(DEPLOYMENT.BASE),
    }
