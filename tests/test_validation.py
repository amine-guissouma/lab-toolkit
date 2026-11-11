



from lab_toolkit.deployment.validation import (
    validate_branch,
    validate_config,
    validate_expected_fields,
    validate_paths,
    validate_required_fields,
)

EXPECTED_REMOTE = "/var/www/labs/lab-front-react/socle"
EXPECTED_BASE = "/"


"z"
def test_validate_required_fields_valid():
    """Vérifie une configuration avec tous les paramètres."""

    config = {
        "remoteDir": EXPECTED_REMOTE,
        "base": EXPECTED_BASE,
    }

    assert validate_required_fields(config) == []


def test_validate_required_fields_missing():
    """Vérifie la détection d'un paramètre manquant."""

    config = {
        "remoteDir": EXPECTED_REMOTE,
    }

    errors = validate_required_fields(config)

    assert len(errors) == 1
    assert "base" in errors[0]


def test_validate_required_fields_wrong_type():
    """Vérifie le rejet d'un paramètre qui n'est pas une chaîne."""

    config = {
        "remoteDir": 123,
        "base": EXPECTED_BASE,
    }

    errors = validate_required_fields(config)

    assert len(errors) == 1
    assert "remoteDir" in errors[0]


def test_validate_required_fields_empty():
    """Vérifie le rejet d'un paramètre vide."""

    config = {
        "remoteDir": EXPECTED_REMOTE,
        "base": "   ",
    }

    errors = validate_required_fields(config)

    assert len(errors) == 1
    assert "base" in errors[0]


def test_validate_branch_socle():
    """Vérifie que la branche socle est autorisée."""

    assert validate_branch("socle") == []


def test_validate_branch_experience_nested():
    """Vérifie qu'une branche d'expérience imbriquée est autorisée."""

    assert validate_branch("experience/auth/token") == []


def test_validate_branch_experience_empty():
    """Vérifie le rejet d'une branche experience sans sujet."""

    assert validate_branch("experience/") != []


def test_validate_branch_unknown():
    """Vérifie le rejet d'une branche non prise en charge."""

    assert validate_branch("master") != []


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
    ) == []


def test_validate_paths_invalid():
    """Vérifie la détection de chemins incorrects."""

    config = {
        "remoteDir": "/var/www/incorrect",
        "base": "/incorrect/",
    }

    errors = validate_paths(
        config,
        EXPECTED_REMOTE,
        EXPECTED_BASE,
    )

    assert len(errors) == 2


def test_validate_config_socle():
    """Vérifie la validation complète d'une configuration socle."""

    config = {
        "remoteDir": EXPECTED_REMOTE,
        "base": EXPECTED_BASE,
    }

    assert validate_config(
        config,
        EXPECTED_REMOTE,
        EXPECTED_BASE,
    ) == []


def test_validate_config_experience_nested():
    """Vérifie la validation complète d'une expérience imbriquée."""

    config = {
        "remoteDir": "/var/www/labs/lab-front-react/experiences/auth/token",
        "base": "/experiences/auth/token/",
    }

    assert validate_config(
        config,
        "/var/www/labs/lab-front-react/experiences/auth/token",
        "/experiences/auth/token/",
    ) == []


## validate_expected_fields

def test_validate_expected_fields_valid():
    """Vérifie une configuration attendue valide."""

    config = {
        "expectedRemoteDir": "/var/www/labs/lab-front-react",
    }

    assert validate_expected_fields(config) == []


def test_validate_expected_fields_missing():
    """Vérifie la détection du paramètre manquant."""

    config = {}

    errors = validate_expected_fields(config)

    assert len(errors) == 1
    assert "expectedRemoteDir" in errors[0]


def test_validate_expected_fields_wrong_type():
    """Vérifie le rejet d'un paramètre qui n'est pas une chaîne."""

    config = {
        "expectedRemoteDir": 123,
    }

    errors = validate_expected_fields(config)

    assert len(errors) == 1
    assert "expectedRemoteDir" in errors[0]


def test_validate_expected_fields_empty():
    """Vérifie le rejet d'un paramètre vide."""

    config = {
        "expectedRemoteDir": "   ",
    }

    errors = validate_expected_fields(config)

    assert len(errors) == 1
    assert "expectedRemoteDir" in errors[0]

def test_validate_expected_fields_relative_path():
    config = {
        "expectedRemoteDir": "var/www/labs/lab-front-react"
    }

    errors = validate_expected_fields(config)

    assert errors == [
        "Le paramètre expectedRemoteDir doit être un chemin absolu."
    ]

def test_validate_expected_fields_path_with_surrounding_spaces():
    config = {
        "expectedRemoteDir": " /var/www/labs/lab-front-react "
    }

    errors = validate_expected_fields(config)

    assert errors == [
        "Le paramètre expectedRemoteDir ne doit pas contenir "
        "d'espaces au début ou à la fin."
    ]