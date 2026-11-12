
from unittest.mock import patch

import pytest

from lab_toolkit.exceptions import (
    BranchError,
    ConfigurationError,
)
from lab_toolkit.deployment.pipeline_validation import validate_pipeline


@patch("lab_toolkit.deployment.pipeline_validation.validate_paths")
@patch("lab_toolkit.deployment.pipeline_validation.build_expected_paths")
@patch("lab_toolkit.deployment.pipeline_validation.get_current_branch")
@patch("lab_toolkit.deployment.pipeline_validation.validate_expected_fields")
@patch("lab_toolkit.deployment.pipeline_validation.load_expected_config")
@patch("lab_toolkit.deployment.pipeline_validation.validate_required_fields")
@patch("lab_toolkit.deployment.pipeline_validation.load_config")
def test_validate_pipeline_success(
    mock_load_config,
    mock_validate_required,
    mock_load_expected,
    mock_validate_expected,
    mock_get_branch,
    mock_build_paths,
    mock_validate_paths,
):
    mock_load_config.return_value = {
        "remoteDir": "/var/www/labs/socle",
        "base": "/",
    }
    mock_load_expected.return_value = {
        "expectedRemoteDir": "/var/www/labs",
    }
    mock_get_branch.return_value = "socle"
    mock_build_paths.return_value = (
        "/var/www/labs/socle",
        "/",
    )

    validate_pipeline()

    mock_load_config.assert_called_once()
    mock_validate_required.assert_called_once()
    mock_load_expected.assert_called_once()
    mock_validate_expected.assert_called_once()
    mock_get_branch.assert_called_once()
    mock_build_paths.assert_called_once_with(
        "socle",
        "/var/www/labs",
    )
    mock_validate_paths.assert_called_once()


@patch("lab_toolkit.deployment.pipeline_validation.validate_required_fields")
@patch("lab_toolkit.deployment.pipeline_validation.load_config")
def test_validate_pipeline_stops_if_config_is_invalid(
    mock_load_config,
    mock_validate_required,
):
    mock_load_config.return_value = {}

    mock_validate_required.side_effect = ConfigurationError(
        ["Paramètre manquant : base"]
    )

    with pytest.raises(ConfigurationError):
        validate_pipeline()

    mock_validate_required.assert_called_once()


@patch("lab_toolkit.deployment.pipeline_validation.validate_expected_fields")
@patch("lab_toolkit.deployment.pipeline_validation.load_expected_config")
@patch("lab_toolkit.deployment.pipeline_validation.validate_required_fields")
@patch("lab_toolkit.deployment.pipeline_validation.load_config")
def test_validate_pipeline_stops_if_expected_config_is_invalid(
    mock_load_config,
    mock_validate_required,
    mock_load_expected,
    mock_validate_expected,
):
    mock_load_config.return_value = {
        "remoteDir": "/var/www/labs/socle",
        "base": "/",
    }
    mock_load_expected.return_value = {}

    mock_validate_expected.side_effect = ConfigurationError(
        ["Paramètre attendu manquant : expectedRemoteDir"]
    )

    with pytest.raises(ConfigurationError):
        validate_pipeline()

    mock_validate_expected.assert_called_once()


@patch("lab_toolkit.deployment.pipeline_validation.get_current_branch")
@patch("lab_toolkit.deployment.pipeline_validation.validate_expected_fields")
@patch("lab_toolkit.deployment.pipeline_validation.load_expected_config")
@patch("lab_toolkit.deployment.pipeline_validation.validate_required_fields")
@patch("lab_toolkit.deployment.pipeline_validation.load_config")
def test_validate_pipeline_stops_if_branch_is_invalid(
    mock_load_config,
    mock_validate_required,
    mock_load_expected,
    mock_validate_expected,
    mock_get_branch,
):
    mock_load_config.return_value = {
        "remoteDir": "/var/www/labs/socle",
        "base": "/",
    }
    mock_load_expected.return_value = {
        "expectedRemoteDir": "/var/www/labs",
    }
    mock_get_branch.return_value = "master"

    with patch(
        "lab_toolkit.deployment.pipeline_validation.build_expected_paths",
        side_effect=BranchError(["Branche Git non prise en charge : master"]),
    ):
        with pytest.raises(BranchError):
            validate_pipeline()


@patch("lab_toolkit.deployment.pipeline_validation.validate_paths")
@patch("lab_toolkit.deployment.pipeline_validation.build_expected_paths")
@patch("lab_toolkit.deployment.pipeline_validation.get_current_branch")
@patch("lab_toolkit.deployment.pipeline_validation.validate_expected_fields")
@patch("lab_toolkit.deployment.pipeline_validation.load_expected_config")
@patch("lab_toolkit.deployment.pipeline_validation.validate_required_fields")
@patch("lab_toolkit.deployment.pipeline_validation.load_config")
def test_validate_pipeline_stops_if_paths_are_invalid(
    mock_load_config,
    mock_validate_required,
    mock_load_expected,
    mock_validate_expected,
    mock_get_branch,
    mock_build_paths,
    mock_validate_paths,
):
    mock_load_config.return_value = {
        "remoteDir": "/var/www/labs/incorrect",
        "base": "/incorrect/",
    }
    mock_load_expected.return_value = {
        "expectedRemoteDir": "/var/www/labs",
    }
    mock_get_branch.return_value = "socle"
    mock_build_paths.return_value = (
        "/var/www/labs/socle",
        "/",
    )

    mock_validate_paths.side_effect = ConfigurationError(
        ["remoteDir incorrect"]
    )

    with pytest.raises(ConfigurationError):
        validate_pipeline()

    mock_validate_paths.assert_called_once()
