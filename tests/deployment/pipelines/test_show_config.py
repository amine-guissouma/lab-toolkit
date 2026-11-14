from tests.tools.pipline_tools_test import (
    MockConfig,
    assert_mock,
    mocks_function,
)

from lab_toolkit.deployment.constants import BRANCH, DEPLOYMENT
from lab_toolkit.deployment.pipeline import show_config

CURRENT_CONFIG_REMOTE_DIR = "/var/www/labs/test-project"

CURRENT_CONFIG = {
    DEPLOYMENT.REMOTE_DIR: "/var/www/labs/test-project",
    DEPLOYMENT.BASE: "/",
    "description": "Configuration de test",
}

EXPECTED_REMOTE_DIR = "/var/www/labs/lab-front-react"
PROPOSED_CONFIG = {
    DEPLOYMENT.REMOTE_DIR: f"{EXPECTED_REMOTE_DIR}/{BRANCH.SOCLE}",
    DEPLOYMENT.BASE: "/",
}


def test_show_config_pipeline_displays_configuration(monkeypatch, capsys):
    # Prepare
    mocks = [
        MockConfig(
            name="load_config",
            return_value=CURRENT_CONFIG,
        ),
        MockConfig(
            name="build_deployment_config",
            return_value=PROPOSED_CONFIG,
        ),
    ]

    mocks_function(show_config, mocks, monkeypatch)

    # Execute
    show_config.show_config_pipeline()

    # Test
    output = capsys.readouterr().out

    assert_mock(mocks)

    assert "Configuration actuelle :" in output
    assert "Configuration proposée :" in output
    assert CURRENT_CONFIG_REMOTE_DIR in output
    assert f"{EXPECTED_REMOTE_DIR}/{BRANCH.SOCLE}" in output
    assert "Aucune modification effectuée." in output


def test_show_config_pipeline_does_not_modify_current_config(
    monkeypatch,
):
    # Prepare
    original_config = CURRENT_CONFIG.copy()

    mocks = [
        MockConfig(
            name="load_config",
            return_value=CURRENT_CONFIG,
        ),
        MockConfig(
            name="build_deployment_config",
            return_value=PROPOSED_CONFIG,
        ),
    ]

    mocks_function(show_config, mocks, monkeypatch)

    # Execute
    show_config.show_config_pipeline()

    # Test
    assert_mock(mocks)
    assert original_config == CURRENT_CONFIG
