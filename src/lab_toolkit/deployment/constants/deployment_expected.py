from dataclasses import dataclass


@dataclass(frozen=True)
class DeploymentExpectedConstants:
    """Constantes associées au fichier deployment_expected.json."""

    FILENAME: str = "deployment_expected.json"
    EXPECTED_REMOTE_DIR: str = "expectedRemoteDir"

    DEFAULT_EXPECTED_REMOTE_DIR: str = "/var/www/labs/un-configured"


DEPLOYMENT_EXPECTED = DeploymentExpectedConstants()
