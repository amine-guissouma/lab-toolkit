from lab_toolkit.exceptions import BranchError
import pytest

from lab_toolkit.deployment.paths import build_expected_paths


EXPECTED_REMOTE_DIR = "/var/www/labs/lab-front-react"


def test_build_expected_paths_socle():
    """Vérifie les chemins attendus pour la branche socle."""

    expected_remote, expected_base = build_expected_paths(
        "socle",
        EXPECTED_REMOTE_DIR,
    )

    assert expected_remote == (
        "/var/www/labs/lab-front-react/socle"
    )
    assert expected_base == "/"


def test_build_expected_paths_experience():
    """Vérifie les chemins d'une branche d'expérience."""

    expected_remote, expected_base = build_expected_paths(
        "experience/mon-experience",
        EXPECTED_REMOTE_DIR,
    )

    assert expected_remote == (
        "/var/www/labs/lab-front-react/experiences/mon-experience"
    )
    assert expected_base == "/experiences/mon-experience/"


def test_build_expected_paths_nested_experience():
    """Vérifie les chemins d'une branche d'expérience imbriquée."""

    expected_remote, expected_base = build_expected_paths(
        "experience/auth/token",
        EXPECTED_REMOTE_DIR,
    )

    assert expected_remote == (
        "/var/www/labs/lab-front-react/experiences/auth/token"
    )
    assert expected_base == "/experiences/auth/token/"


def test_build_expected_paths_preserves_branch_name():
    """Vérifie que le nom de la branche est conservé exactement."""

    expected_remote, expected_base = build_expected_paths(
        "experience/auth/mon-experience",
        EXPECTED_REMOTE_DIR,
    )

    assert expected_remote.endswith(
        "/experiences/auth/mon-experience"
    )
    assert expected_base == "/experiences/auth/mon-experience/"


@pytest.mark.parametrize(
    "branch",
    [
        "master",
        "experience/",
        "experience//token",
        "feature/test",
    ],
)
def test_build_expected_paths_invalid_branch(branch):
    with pytest.raises(BranchError):
        build_expected_paths(
            branch,
            "/var/www/labs/lab-front-react",
        )