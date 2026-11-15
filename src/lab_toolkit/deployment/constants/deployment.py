from dataclasses import dataclass


@dataclass(frozen=True)
class DeploymentConstants:
    """Constantes associées au fichier deployment.json."""

    FILENAME: str = "deployment.json"

    REMOTE_DIR: str = "remoteDir"
    BASE: str = "base"

    DEFAULT_REMOTE_DIR: str = "socle"
    DEFAULT_BASE: str = "/"

    EXPERIENCES_DIR: str = "experiences"


DEPLOYMENT = DeploymentConstants()
