import json

import pytest
from _pytest.monkeypatch import MonkeyPatch

from lab_toolkit.deployment import configuration
from lab_toolkit.deployment.constants import BRANCH, DEPLOYMENT, DEPLOYMENT_EXPECTED
from lab_toolkit.exceptions import ConfigurationError

EXPECTED_REMOTE_DIR = "/var/www/labs/lab-front-react"


# helper
def pach_get_current_branch(monkeypatch: MonkeyPatch, branch: str):
    monkeypatch.setattr(
        configuration,
        "get_current_branch",
        lambda: branch,
    )


def create_expected_config(tmp_path):
    config = {DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR: EXPECTED_REMOTE_DIR}

    config_path = tmp_path / DEPLOYMENT_EXPECTED.FILENAME
    config_path.write_text(
        json.dumps(config),
        encoding="utf-8",
    )


# tests
def test_build_deployment_config_socle(tmp_path, monkeypatch):
    # prepare
    create_expected_config(tmp_path)
    pach_get_current_branch(monkeypatch, BRANCH.SOCLE)

    # execute
    result = configuration.build_deployment_config(tmp_path)

    # tests
    assert result == {
        DEPLOYMENT.REMOTE_DIR: f"{EXPECTED_REMOTE_DIR}/{BRANCH.SOCLE}",
        DEPLOYMENT.BASE: "/",
    }


def test_build_deployment_config_nested_experience(tmp_path, monkeypatch):
    # prepare
    create_expected_config(tmp_path)
    branch = "auth/token"
    pach_get_current_branch(monkeypatch, f"{BRANCH.EXPERIENCE_PREFIX}{branch}")

    # execute
    result = configuration.build_deployment_config(tmp_path)

    # tests
    assert result == {
        DEPLOYMENT.REMOTE_DIR: (
            f"{EXPECTED_REMOTE_DIR}/{DEPLOYMENT.EXPERIENCES_DIR}/{branch}"
        ),
        DEPLOYMENT.BASE: f"/{DEPLOYMENT.EXPERIENCES_DIR}/{branch}/",
    }


def test_build_deployment_config_invalid_expected_config(
    tmp_path,
    monkeypatch,
):
    # prepare
    config_path = tmp_path / DEPLOYMENT_EXPECTED.FILENAME
    config_path.write_text("{}", encoding="utf-8")

    pach_get_current_branch(monkeypatch, BRANCH.SOCLE)

    # test raise
    with pytest.raises(ConfigurationError):
        # execute
        configuration.build_deployment_config(tmp_path)


def test_build_deployment_config_with_explicit_branch(tmp_path):
    # prepare
    create_expected_config(tmp_path)
    # execute
    result = configuration.build_deployment_config(
        project_dir=tmp_path,
        branch=BRANCH.SOCLE,
    )
    # test
    assert result == {
        DEPLOYMENT.REMOTE_DIR: f"{EXPECTED_REMOTE_DIR}/{BRANCH.SOCLE}",
        DEPLOYMENT.BASE: "/",
    }
