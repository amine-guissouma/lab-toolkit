from tests.tools.pipline_tools_test import (
    MockConfig,
    assert_mock,
    mocks_function,
)

from lab_toolkit.deployment.pipeline import show_config

CURRENT_CONFIG = {
    "remoteDir": "/var/www/labs/test-project",
    "base": "/",
    "description": "Configuration de test",
}

PROPOSED_CONFIG = {
    "remoteDir": "/var/www/labs/lab-front-react/socle",
    "base": "/",
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
    assert "/var/www/labs/test-project" in output
    assert "/var/www/labs/lab-front-react/socle" in output
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
