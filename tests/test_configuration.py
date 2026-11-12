
import json

import pytest

from lab_toolkit.deployment import configuration
from lab_toolkit.exceptions import ConfigurationError


def create_expected_config(tmp_path):
    config = {
        "expectedRemoteDir": "/var/www/labs/lab-front-react"
    }

    config_path = tmp_path / "deployment_expected.json"
    config_path.write_text(
        json.dumps(config),
        encoding="utf-8",
    )


def test_build_deployment_config_socle(tmp_path, monkeypatch):
    create_expected_config(tmp_path)

    monkeypatch.setattr(
        configuration,
        "get_current_branch",
        lambda: "socle",
    )

    result = configuration.build_deployment_config(tmp_path)

    assert result == {
        "remoteDir": "/var/www/labs/lab-front-react/socle",
        "base": "/",
    }


def test_build_deployment_config_nested_experience(tmp_path, monkeypatch):
    create_expected_config(tmp_path)

    monkeypatch.setattr(
        configuration,
        "get_current_branch",
        lambda: "experience/auth/token",
    )

    result = configuration.build_deployment_config(tmp_path)

    assert result == {
        "remoteDir": (
            "/var/www/labs/lab-front-react/"
            "experiences/auth/token"
        ),
        "base": "/experiences/auth/token/",
    }


def test_build_deployment_config_invalid_expected_config(
    tmp_path,
    monkeypatch,
):
    config_path = tmp_path / "deployment_expected.json"
    config_path.write_text("{}", encoding="utf-8")

    monkeypatch.setattr(
        configuration,
        "get_current_branch",
        lambda: "socle",
    )

    with pytest.raises(ConfigurationError):
        configuration.build_deployment_config(tmp_path)

def test_build_deployment_config_with_explicit_branch(tmp_path):
    create_expected_config(tmp_path)

    result = configuration.build_deployment_config(
        project_dir=tmp_path,
        branch="socle",
    )

    assert result == {
        "remoteDir": "/var/www/labs/lab-front-react/socle",
        "base": "/",
    }
