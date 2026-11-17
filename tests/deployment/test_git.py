import subprocess

import pytest

from lab_toolkit.deployment import git
from lab_toolkit.deployment.constants import BRANCH
from lab_toolkit.deployment.git import get_current_branch, local_branch_exists
from lab_toolkit.exceptions import GitError


def test_get_current_branch(monkeypatch):
    """Vérifie la récupération du nom de la branche."""
    # prepare
    stdout = BRANCH.SOCLE

    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args[0],
            returncode=0,
            stdout=stdout,
            stderr="",
        )

    monkeypatch.setattr("subprocess.run", mock_run)

    # execute
    result = get_current_branch()

    # tests
    assert result == BRANCH.SOCLE


def test_get_current_branch_empty(monkeypatch):
    """Vérifie le rejet d'un nom de branche vide."""

    # prepare
    stdout = "\n"

    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args[0],
            returncode=0,
            stdout=stdout,
            stderr="",
        )

    monkeypatch.setattr("subprocess.run", mock_run)

    # execute / test
    with pytest.raises(GitError):
        get_current_branch()


def test_local_branch_exists(monkeypatch):
    """Vérifie la détection d'une branche locale existante."""

    # prepare
    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args[0],
            returncode=0,
            stdout="",
            stderr="",
        )

    monkeypatch.setattr(git.subprocess, "run", mock_run)

    # result
    result = local_branch_exists(BRANCH.SOCLE)

    # test
    assert result is True


def test_local_branch_does_not_exist(monkeypatch):
    """Vérifie la détection d'une branche locale absente."""

    # prepare
    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args[0],
            returncode=1,
            stdout="",
            stderr="",
        )

    monkeypatch.setattr(git.subprocess, "run", mock_run)

    # execute
    result = local_branch_exists(BRANCH.SOCLE)

    # tests
    assert result is False


def test_local_branch_exists_git_error(monkeypatch):
    """Vérifie la gestion d'une erreur Git inattendue."""

    # prepare
    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args[0],
            returncode=128,
            stdout="",
            stderr="Erreur Git",
        )

    monkeypatch.setattr(git.subprocess, "run", mock_run)

    # execute / test
    with pytest.raises(GitError):
        git.local_branch_exists(BRANCH.SOCLE)


def test_get_current_branch_git_error(monkeypatch):
    # prepare
    def mock_run(*args, **kwargs):
        raise subprocess.CalledProcessError(
            returncode=128,
            cmd=args[0],
            stderr="Erreur Git",
        )

    monkeypatch.setattr(
        subprocess,
        subprocess.run.__name__,
        mock_run,
    )

    # execute / test
    with pytest.raises(GitError):
        get_current_branch()
