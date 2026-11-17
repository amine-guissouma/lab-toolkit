from tests.tools.pipline_tools_test import (
    MockConfig,
    assert_mock,
    mocks_function,
)

from lab_toolkit.deployment.config import load_config
from lab_toolkit.deployment.configuration import build_deployment_config
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


def test_show_config_pipeline_does_not_modify_current_config(
    monkeypatch,
):
    # Prepare
    original_config = CURRENT_CONFIG.copy()

    mocks = [
        MockConfig(
            name=load_config.__name__,
            return_value=CURRENT_CONFIG,
        ),
        MockConfig(
            name=build_deployment_config.__name__,
            return_value=PROPOSED_CONFIG,
        ),
    ]

    mocks_function(show_config, mocks, monkeypatch)

    # Execute
    show_config.show_config_pipeline()

    # Test
    assert_mock(mocks)
    assert original_config == CURRENT_CONFIG


def test_show_config_pipeline_returns_current_and_proposed_configuration(
    monkeypatch,
):
    # prepare
    mocks = [
        MockConfig(
            name=load_config.__name__,
            return_value=CURRENT_CONFIG,
        ),
        MockConfig(
            name=build_deployment_config.__name__,
            return_value=PROPOSED_CONFIG,
        ),
    ]

    mocks_function(show_config, mocks, monkeypatch)

    # execute
    result = show_config.show_config_pipeline()

    # test
    assert_mock(mocks)
    assert isinstance(result, dict)
    assert result
