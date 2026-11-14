import pytest
from tests.tools.pipline_tools_test import MockConfig, assert_mock, mocks_function

from lab_toolkit.deployment.pipeline import validation_config
from lab_toolkit.exceptions import BranchError, ConfigurationError


def test_validate_pipeline_success(monkeypatch):
    # prepare
    mocks = [
        MockConfig(
            name="load_config",
            return_value={"remoteDir": "/var/www/labs/socle", "base": "/"},
        ),
        MockConfig(
            name="validate_required_fields",
        ),
        MockConfig(
            name="load_expected_config",
            return_value={
                "expectedRemoteDir": "/var/www/labs",
            },
        ),
        MockConfig(name="validate_expected_fields"),
        MockConfig(
            name="get_current_branch",
            return_value="socle",
        ),
        MockConfig(
            name="build_expected_paths",
            return_value=(
                "/var/www/labs/socle",
                "/",
            ),
            expected_args=("socle", "/var/www/labs"),
        ),
        MockConfig(name="validate_paths"),
    ]
    mocks_function(validation_config, mocks, monkeypatch)
    # execute
    validation_config.validate_pipeline()
    # test
    assert_mock(mocks)


def test_validate_pipeline_stops_if_config_is_invalid(monkeypatch):
    # prepare
    mocks = [
        MockConfig(name="load_config", return_value={}),
        MockConfig(
            name="validate_required_fields",
            side_effect=ConfigurationError(["Paramètre manquant : base"]),
        ),
    ]
    mocks_function(validation_config, mocks, monkeypatch)

    # execute
    with pytest.raises(ConfigurationError):
        validation_config.validate_pipeline()

    assert_mock(mocks)


def test_validate_pipeline_stops_if_expected_config_is_invalid(monkeypatch):
    # prepare
    mocks = [
        MockConfig(
            "load_config",
            return_value={
                "remoteDir": "/var/www/labs/socle",
                "base": "/",
            },
        ),
        MockConfig("validate_required_fields"),
        MockConfig("load_expected_config", return_value={}),
        MockConfig(
            "validate_expected_fields",
            side_effect=ConfigurationError(
                ["Paramètre attendu manquant : expectedRemoteDir"]
            ),
        ),
    ]
    mocks_function(validation_config, mocks, monkeypatch)

    # execute
    with pytest.raises(ConfigurationError):
        validation_config.validate_pipeline()

    # test
    assert_mock(mocks)


def test_validate_pipeline_stops_if_branch_is_invalid(monkeypatch):
    # prepare
    mocks = [
        MockConfig(
            "load_config",
            return_value={
                "remoteDir": "/var/www/labs/socle",
                "base": "/",
            },
        ),
        MockConfig(
            "validate_required_fields",
        ),
        MockConfig(
            "load_expected_config",
            return_value={
                "expectedRemoteDir": "/var/www/labs",
            },
        ),
        MockConfig(
            "validate_expected_fields",
        ),
        MockConfig("get_current_branch", return_value="master"),
        MockConfig(
            "build_expected_paths",
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
            "load_config",
            return_value={
                "remoteDir": "/var/www/labs/incorrect",
                "base": "/incorrect/",
            },
        ),
        MockConfig(
            "validate_required_fields",
        ),
        MockConfig(
            "load_expected_config",
            return_value={
                "expectedRemoteDir": "/var/www/labs",
            },
        ),
        MockConfig(
            "validate_expected_fields",
        ),
        MockConfig("get_current_branch", return_value="socle"),
        MockConfig(
            "build_expected_paths",
            return_value=(
                "/var/www/labs/socle",
                "/",
            ),
        ),
        MockConfig(
            "validate_paths", side_effect=ConfigurationError(["remoteDir incorrect"])
        ),
    ]
    mocks_function(validation_config, mocks, monkeypatch)

    # execute
    with pytest.raises(ConfigurationError):
        validation_config.validate_pipeline()

    # test
    assert_mock(mocks)
