from dataclasses import dataclass


@dataclass(frozen=True)
class DeploymentExpectedConstants:
    """Constantes associées au fichier deployment_expected.json."""

    FILENAME: str = "deployment_expected.json"
    EXPECTED_REMOTE_DIR: str = "expectedRemoteDir"


DEPLOYMENT_EXPECTED = DeploymentExpectedConstants()
