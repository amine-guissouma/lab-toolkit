import pytest
from tests.tools.pipline_tools_test import MockConfig, assert_mock, mocks_function

from lab_toolkit.deployment.config import load_config, load_expected_config
from lab_toolkit.deployment.constants import BRANCH, DEPLOYMENT, DEPLOYMENT_EXPECTED
from lab_toolkit.deployment.git import get_current_branch
from lab_toolkit.deployment.paths import build_expected_paths
from lab_toolkit.deployment.pipeline import validation_config
from lab_toolkit.deployment.validation import (
    validate_expected_fields,
    validate_paths,
    validate_required_fields,
)
from lab_toolkit.exceptions import BranchError, ConfigurationError


def test_validate_pipeline_success(monkeypatch):
    # prepare
    mocks = [
        MockConfig(
            name=load_config.__name__,
            return_value={
                DEPLOYMENT.REMOTE_DIR: "/var/www/labs/socle",
                DEPLOYMENT.BASE: "/",
            },
        ),
        MockConfig(
            name=validate_required_fields.__name__,
        ),
        MockConfig(
            name=load_expected_config.__name__,
            return_value={
                DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR: "/var/www/labs",
            },
        ),
        MockConfig(name=validate_expected_fields.__name__),
        MockConfig(
            name=get_current_branch.__name__,
            return_value=BRANCH.SOCLE,
        ),
        MockConfig(
            name=build_expected_paths.__name__,
            return_value=(
                "/var/www/labs/socle",
                "/",
            ),
            expected_args=(BRANCH.SOCLE, "/var/www/labs"),
        ),
        MockConfig(name=validate_paths.__name__),
    ]
    mocks_function(validation_config, mocks, monkeypatch)
    # execute
    result = validation_config.validate_pipeline()
    # test
    assert_mock(mocks)
    assert result is not None


def test_validate_pipeline_stops_if_config_is_invalid(monkeypatch):
    # prepare
    mocks = [
        MockConfig(name="load_config", return_value={}),
        MockConfig(
            name=validate_required_fields.__name__,
            side_effect=ConfigurationError([f"Paramètre manquant : {DEPLOYMENT.BASE}"]),
        ),
    ]

    mocks_function(validation_config, mocks, monkeypatch)

    # execute / test
    with pytest.raises(ConfigurationError):
        validation_config.validate_pipeline()

    # test
    assert_mock(mocks)


def test_validate_pipeline_stops_if_expected_config_is_invalid(monkeypatch):
    # prepare
    mocks = [
        MockConfig(
            load_config.__name__,
            return_value={
                DEPLOYMENT.REMOTE_DIR: "/var/www/labs/socle",
                DEPLOYMENT.BASE: "/",
            },
        ),
        MockConfig(validate_required_fields.__name__),
        MockConfig("load_expected_config", return_value={}),
        MockConfig(
            validate_expected_fields.__name__,
            side_effect=ConfigurationError(
                [
                    f"Paramètre attendu manquant : {DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR}"
                ]
            ),
        ),
    ]

    mocks_function(validation_config, mocks, monkeypatch)

    # execute / test
    with pytest.raises(ConfigurationError):
        validation_config.validate_pipeline()

    # test
    assert_mock(mocks)


def test_validate_pipeline_stops_if_branch_is_invalid(monkeypatch):
    # prepare
    mocks = [
        MockConfig(
            load_config.__name__,
            return_value={
                DEPLOYMENT.REMOTE_DIR: "/var/www/labs/socle",
                DEPLOYMENT.BASE: "/",
            },
        ),
        MockConfig(
            validate_required_fields.__name__,
        ),
        MockConfig(
            load_expected_config.__name__,
            return_value={
                DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR: "/var/www/labs",
            },
        ),
        MockConfig(
            validate_expected_fields.__name__,
        ),
        MockConfig(get_current_branch.__name__, return_value="master"),
        MockConfig(
            build_expected_paths.__name__,
            side_effect=BranchError(["Branche Git non prise en charge : master"]),
        ),
    ]

    mocks_function(validation_config, mocks, monkeypatch)

    # execute
    with pytest.raises(BranchError):
        validation_config.validate_pipeline()

    # test
    assert_mock(mocks)


def test_validate_pipeline_stops_if_paths_are_invalid(monkeypatch):
    # prepare
    mocks = [
        MockConfig(
            load_config.__name__,
            return_value={
                DEPLOYMENT.REMOTE_DIR: "/var/www/labs/incorrect",
                DEPLOYMENT.BASE: "/incorrect/",
            },
        ),
        MockConfig(
            validate_required_fields.__name__,
        ),
        MockConfig(
            "load_expected_config",
            return_value={
                DEPLOYMENT_EXPECTED.EXPECTED_REMOTE_DIR: "/var/www/labs",
            },
        ),
        MockConfig(
            validate_expected_fields.__name__,
        ),
        MockConfig(get_current_branch.__name__, return_value=BRANCH.SOCLE),
        MockConfig(
            build_expected_paths.__name__,
            return_value=(
                "/var/www/labs/socle",
                "/",
            ),
        ),
        MockConfig(
            validate_paths.__name__,
            side_effect=ConfigurationError([f"{DEPLOYMENT.REMOTE_DIR} incorrect"]),
        ),
    ]

    mocks_function(validation_config, mocks, monkeypatch)

    # execute / test
    with pytest.raises(ConfigurationError):
        validation_config.validate_pipeline()

    # test
    assert_mock(mocks)
