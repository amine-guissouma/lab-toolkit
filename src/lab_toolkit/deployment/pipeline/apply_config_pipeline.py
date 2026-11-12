from lab_toolkit.deployment.config import load_config, save_config
from lab_toolkit.deployment.configuration import build_deployment_config


def apply_config_pipeline() -> None:
    """Calcule et enregistre la configuration de déploiement."""
    current_config = load_config()

    new_config = {
        **current_config,
        **build_deployment_config(),
    }

    save_config(new_config)

    print(f"  remoteDir : {new_config['remoteDir']}")
    print(f"  base      : {new_config['base']}")
