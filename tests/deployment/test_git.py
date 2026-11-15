import subprocess

import pytest

from lab_toolkit.deployment.constants import BRANCH
from lab_toolkit.deployment.git import get_current_branch
from lab_toolkit.exceptions import GitError


def test_get_current_branch(monkeypatch):
    """Vérifie la récupération du nom de la branche."""

    stdout = BRANCH.SOCLE

    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args[0],
            returncode=0,
            stdout=stdout,
            stderr="",
        )

    monkeypatch.setattr("subprocess.run", mock_run)

    assert get_current_branch() == BRANCH.SOCLE


def test_get_current_branch_empty(monkeypatch):
    """Vérifie le rejet d'un nom de branche vide."""

    stdout = "\n"

    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args[0],
            returncode=0,
            stdout=stdout,
            stderr="",
        )

    monkeypatch.setattr("subprocess.run", mock_run)

    with pytest.raises(GitError):
        get_current_branch()


def test_local_branch_exists(monkeypatch):
    """Vérifie la détection d'une branche locale existante."""

    from lab_toolkit.deployment import git

    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args[0],
            returncode=0,
            stdout="",
            stderr="",
        )

    monkeypatch.setattr(git.subprocess, "run", mock_run)

    assert git.local_branch_exists(BRANCH.SOCLE) is True


def test_local_branch_does_not_exist(monkeypatch):
    """Vérifie la détection d'une branche locale absente."""

    from lab_toolkit.deployment import git

    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args[0],
            returncode=1,
            stdout="",
            stderr="",
        )

    monkeypatch.setattr(git.subprocess, "run", mock_run)

    assert git.local_branch_exists(BRANCH.SOCLE) is False


def test_local_branch_exists_git_error(monkeypatch):
    """Vérifie la gestion d'une erreur Git inattendue."""

    from lab_toolkit.deployment import git

    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args[0],
            returncode=128,
            stdout="",
            stderr="Erreur Git",
        )

    monkeypatch.setattr(git.subprocess, "run", mock_run)

    with pytest.raises(GitError):
        git.local_branch_exists(BRANCH.SOCLE)
