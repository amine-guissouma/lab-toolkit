import pytest

from lab_toolkit.deployment.constants import BRANCH, DEPLOYMENT, DEPLOYMENT_EXPECTED
from lab_toolkit.deployment.validation import (
    validate_branch,
    validate_expected_fields,
    validate_paths,
    validate_required_fields,
)
from lab_toolkit.exceptions import (
    BranchError,
    ConfigurationError,
)

EXPECTED_REMOTE_DIR = "/var/www/labs/lab-front-react"

EXPECTED_REMOTE = f"{EXPECTED_REMOTE_DIR}/{BRANCH.SOCLE}"
EXPECTED_BASE = "/"


# ===== validate_required_fields =====
def test_validate_required_fields_valid():
    """Vérifie une configuration avec tous les paramètres."""

    config = {
        DEPLOYMENT.REMOTE_DIR: EXPECTED_REMOTE,
        DEPLOYMENT.BASE: EXPECTED_BASE,
    }

    assert validate_required_fields(config) is None


def test_validate_required_fields_missing():
    """Vérifie la détection d'un paramètre manquant."""

    config = {
        DEPLOYMENT.REMOTE_DIR: EXPECTED_REMOTE,
    }

    with pytest.raises(ConfigurationError) as error:
        validate_required_fields(config)

    assert len(error.value.errors) == 1
    assert DEPLOYMENT.BASE in error.value.errors[0]


def test_validate_required_fields_wrong_type():
    """Vérifie le rejet d'un paramètre qui n'est pas une chaîne."""

    config = {
        DEPLOYMENT.REMOTE_DIR: 123,
        DEPLOYMENT.BASE: EXPECTED_BASE,
    }

    with pytest.raises(ConfigurationError) as error:
        validate_required_fields(config)

    assert len(error.value.errors) == 1
    assert DEPLOYMENT.REMOTE_DIR in error.value.errors[0]


def test_validate_required_fields_empty():
    """Vérifie le rejet d'un paramètre vide."""

    config = {
        DEPLOYMENT.REMOTE_DIR: EXPECTED_REMOTE,
        DEPLOYMENT.BASE: "   ",
    }

    with pytest.raises(ConfigurationError) as error:
        validate_required_fields(config)

    assert len(error.value.errors) == 1
    assert DEPLOYMENT.BASE in error.value.errors[0]


# ===== validate_branch =====


def test_validate_branch_socle():
    """Vérifie que la branche socle est autorisée."""

    assert validate_branch(BRANCH.SOCLE) is None


def test_validate_branch_experience_nested():
    """Vérifie qu'une branche d'expérience imbriquée est autorisée."""

    assert validate_branch(f"{BRANCH.EXPERIENCE_PREFIX}auth/token") is None


def test_validate_branch_experience_empty():
    """Vérifie le rejet d'une branche experience sans sujet."""

    with pytest.raises(BranchError) as error:
        validate_branch(BRANCH.EXPERIENCE_PREFIX)

    assert len(error.value.errors) == 1
    assert BRANCH.EXPERIENCE_PREFIX in error.value.errors[0]


def test_validate_branch_unknown():
    """Vérifie le rejet d'une branche non prise en charge."""

    with pytest.raises(BranchError) as error:
        validate_branch("master")

    assert len(error.value.errors) == 1
    assert "master" in error.value.errors[0]


# ===== validate_paths =====


def test_validate_paths_valid():
    """Vérifie que les chemins correspondent aux valeurs attendues."""

    config = {
        DEPLOYMENT.REMOTE_DIR: EXPECTED_REMOTE,
        DEPLOYMENT.BASE: EXPECTED_BASE,
    }

    assert (
        validate_paths(
            config,
            EXPECTED_REMOTE,
            EXPECTED_BASE,
        )
        is None
    )


def test_validate_paths_invalid():
    """Vérifie la détection de chemins incorrects."""

    config = {
        DEPLOYMENT.REMOTE_DIR: "/var/www/incorrect",
        DEPLOYMENT.BASE: "/incorrect/",
    }

    with pytest.raises(ConfigurationError) as error:
        validate_paths(
            config,
            EXPECTED_REMOTE,
            EXPECTED_BASE,
        )

    assert len(error.value.errors) == 2
    assert DEPLOYMENT.REMOTE_DIR in error.value.errors[0]
    assert DEPLOYMENT.BASE in error.value.errors[1]


# ===== validate_expected_fields =====


def test_validate_expected_fields_valid():
    """Vérifie une configuration attendue valide."""

    config = {
        DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR: EXPECTED_REMOTE_DIR,
    }

    assert validate_expected_fields(config) is None


def test_validate_expected_fields_missing():
    """Vérifie la détection du paramètre manquant."""

    config = {}

    with pytest.raises(ConfigurationError) as error:
        validate_expected_fields(config)

    assert len(error.value.errors) == 1
    assert DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR in error.value.errors[0]


def test_validate_expected_fields_wrong_type():
    """Vérifie le rejet d'un paramètre qui n'est pas une chaîne."""

    config = {
        DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR: 123,
    }

    with pytest.raises(ConfigurationError) as error:
        validate_expected_fields(config)

    assert len(error.value.errors) == 1
    assert DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR in error.value.errors[0]


def test_validate_expected_fields_empty():
    """Vérifie le rejet d'un paramètre vide."""

    config = {
        DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR: "   ",
    }

    with pytest.raises(ConfigurationError) as error:
        validate_expected_fields(config)

    assert len(error.value.errors) == 1
    assert DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR in error.value.errors[0]


def test_validate_expected_fields_relative_path():
    """Vérifie le rejet d'un chemin relatif."""

    config = {
        DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR: "var/www/labs/lab-front-react",
    }

    with pytest.raises(ConfigurationError) as error:
        validate_expected_fields(config)

    assert len(error.value.errors) == 1
    assert "chemin absolu" in error.value.errors[0]


def test_validate_expected_fields_path_with_surrounding_spaces():
    """Vérifie le rejet des espaces autour du chemin."""

    config = {
        DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR: " /var/www/labs/lab-front-react ",
    }

    with pytest.raises(ConfigurationError) as error:
        validate_expected_fields(config)

    assert len(error.value.errors) == 2
    assert "espaces au début ou à la fin" in error.value.errors[0]
    assert "chemin absolu" in error.value.errors[1]
