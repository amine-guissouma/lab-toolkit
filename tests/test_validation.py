
import pytest

from lab_toolkit.exceptions import (
    BranchError,
    ConfigurationError,
)

from lab_toolkit.deployment.validation import (
    validate_branch,
    validate_expected_fields,
    validate_paths,
    validate_required_fields,
)


EXPECTED_REMOTE = "/var/www/labs/lab-front-react/socle"
EXPECTED_BASE = "/"


# ===== validate_required_fields =====
def test_validate_required_fields_valid():
    """Vérifie une configuration avec tous les paramètres."""

    config = {
        "remoteDir": EXPECTED_REMOTE,
        "base": EXPECTED_BASE,
    }

    assert validate_required_fields(config) is None


def test_validate_required_fields_missing():
    """Vérifie la détection d'un paramètre manquant."""

    config = {
        "remoteDir": EXPECTED_REMOTE,
    }

    with pytest.raises(ConfigurationError) as error:
        validate_required_fields(config)

    assert len(error.value.errors) == 1
    assert "base" in error.value.errors[0]


def test_validate_required_fields_wrong_type():
    """Vérifie le rejet d'un paramètre qui n'est pas une chaîne."""

    config = {
        "remoteDir": 123,
        "base": EXPECTED_BASE,
    }

    with pytest.raises(ConfigurationError) as error:
        validate_required_fields(config)

    assert len(error.value.errors) == 1
    assert "remoteDir" in error.value.errors[0]


def test_validate_required_fields_empty():
    """Vérifie le rejet d'un paramètre vide."""

    config = {
        "remoteDir": EXPECTED_REMOTE,
        "base": "   ",
    }

    with pytest.raises(ConfigurationError) as error:
        validate_required_fields(config)

    assert len(error.value.errors) == 1
    assert "base" in error.value.errors[0]


# ===== validate_branch =====

def test_validate_branch_socle():
    """Vérifie que la branche socle est autorisée."""

    assert validate_branch("socle") is None


def test_validate_branch_experience_nested():
    """Vérifie qu'une branche d'expérience imbriquée est autorisée."""

    assert validate_branch("experience/auth/token") is None


def test_validate_branch_experience_empty():
    """Vérifie le rejet d'une branche experience sans sujet."""

    with pytest.raises(BranchError) as error:
        validate_branch("experience/")

    assert len(error.value.errors) == 1
    assert "experience/" in error.value.errors[0]


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
        "remoteDir": EXPECTED_REMOTE,
        "base": EXPECTED_BASE,
    }

    assert validate_paths(
        config,
        EXPECTED_REMOTE,
        EXPECTED_BASE,
    ) is None


def test_validate_paths_invalid():
    """Vérifie la détection de chemins incorrects."""

    config = {
        "remoteDir": "/var/www/incorrect",
        "base": "/incorrect/",
    }

    with pytest.raises(ConfigurationError) as error:
        validate_paths(
            config,
            EXPECTED_REMOTE,
            EXPECTED_BASE,
        )

    assert len(error.value.errors) == 2
    assert "remoteDir" in error.value.errors[0]
    assert "base" in error.value.errors[1]


# ===== validate_expected_fields =====

def test_validate_expected_fields_valid():
    """Vérifie une configuration attendue valide."""

    config = {
        "expectedRemoteDir": "/var/www/labs/lab-front-react",
    }

    assert validate_expected_fields(config) is None


def test_validate_expected_fields_missing():
    """Vérifie la détection du paramètre manquant."""

    config = {}

    with pytest.raises(ConfigurationError) as error:
        validate_expected_fields(config)

    assert len(error.value.errors) == 1
    assert "expectedRemoteDir" in error.value.errors[0]


def test_validate_expected_fields_wrong_type():
    """Vérifie le rejet d'un paramètre qui n'est pas une chaîne."""

    config = {
        "expectedRemoteDir": 123,
    }

    with pytest.raises(ConfigurationError) as error:
        validate_expected_fields(config)

    assert len(error.value.errors) == 1
    assert "expectedRemoteDir" in error.value.errors[0]


def test_validate_expected_fields_empty():
    """Vérifie le rejet d'un paramètre vide."""

    config = {
        "expectedRemoteDir": "   ",
    }

    with pytest.raises(ConfigurationError) as error:
        validate_expected_fields(config)

    assert len(error.value.errors) == 1
    assert "expectedRemoteDir" in error.value.errors[0]


def test_validate_expected_fields_relative_path():
    """Vérifie le rejet d'un chemin relatif."""

    config = {
        "expectedRemoteDir": "var/www/labs/lab-front-react",
    }

    with pytest.raises(ConfigurationError) as error:
        validate_expected_fields(config)

    assert len(error.value.errors) == 1
    assert "chemin absolu" in error.value.errors[0]


def test_validate_expected_fields_path_with_surrounding_spaces():
    """Vérifie le rejet des espaces autour du chemin."""

    config = {
        "expectedRemoteDir": " /var/www/labs/lab-front-react ",
    }

    with pytest.raises(ConfigurationError) as error:
        validate_expected_fields(config)

    assert len(error.value.errors) == 2
    assert "espaces au début ou à la fin" in error.value.errors[0]
    assert "chemin absolu" in error.value.errors[1]
