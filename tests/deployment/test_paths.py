import pytest

from lab_toolkit.deployment.constants import BRANCH, DEPLOYMENT
from lab_toolkit.deployment.paths import build_expected_paths
from lab_toolkit.exceptions import BranchError

EXPECTED_REMOTE_DIR = "/var/www/labs/lab-front-react"


def test_build_expected_paths_socle():
    """Vérifie les chemins attendus pour la branche socle."""
    # execute
    expected_remote, expected_base = build_expected_paths(
        BRANCH.SOCLE,
        EXPECTED_REMOTE_DIR,
    )
    # test
    assert expected_remote == f"{EXPECTED_REMOTE_DIR}/{BRANCH.SOCLE}"
    assert expected_base == "/"


def test_build_expected_paths_experience():
    """Vérifie les chemins d'une branche d'expérience."""
    # prepare
    branche_experience = "mon-experience"
    branch = f"{BRANCH.EXPERIENCE_PREFIX}{branche_experience}"

    # execute
    expected_remote, expected_base = build_expected_paths(
        branch,
        EXPECTED_REMOTE_DIR,
    )

    # test
    assert (
        expected_remote
        == f"{EXPECTED_REMOTE_DIR}/{DEPLOYMENT.EXPERIENCES_DIR}/{branche_experience}"
    )
    assert expected_base == f"/{DEPLOYMENT.EXPERIENCES_DIR}/{branche_experience}/"


def test_build_expected_paths_nested_experience():
    """Vérifie les chemins d'une branche d'expérience imbriquée."""

    # prepare
    branche_experience = "auth/token"
    branch = f"{BRANCH.EXPERIENCE_PREFIX}{branche_experience}"

    # execute
    expected_remote, expected_base = build_expected_paths(
        branch,
        EXPECTED_REMOTE_DIR,
    )

    # test
    assert (
        expected_remote
        == f"{EXPECTED_REMOTE_DIR}/{DEPLOYMENT.EXPERIENCES_DIR}/{branche_experience}"
    )
    assert expected_base == f"/{DEPLOYMENT.EXPERIENCES_DIR}/{branche_experience}/"


def test_build_expected_paths_preserves_branch_name():
    """Vérifie que le nom de la branche est conservé exactement."""
    # prepare
    branche_experience = "auth/mon-experience"
    branch = f"{BRANCH.EXPERIENCE_PREFIX}{branche_experience}"

    # execute
    expected_remote, expected_base = build_expected_paths(
        branch,
        EXPECTED_REMOTE_DIR,
    )
    # test
    assert expected_remote.endswith(
        f"/{DEPLOYMENT.EXPERIENCES_DIR}/{branche_experience}"
    )
    assert expected_base == f"/{DEPLOYMENT.EXPERIENCES_DIR}/{branche_experience}/"


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
    """Vérifie qu' une erreur 'BranchError' et lever pour une branche incorrect."""

    # test raise BranchError
    with pytest.raises(BranchError):
        # execute
        build_expected_paths(
            branch,
            EXPECTED_REMOTE_DIR,
        )
