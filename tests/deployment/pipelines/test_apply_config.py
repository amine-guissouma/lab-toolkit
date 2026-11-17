from lab_toolkit.deployment.config import load_config, save_config
from lab_toolkit.deployment.configuration import build_deployment_config
from lab_toolkit.deployment.constants import BRANCH, DEPLOYMENT
from lab_toolkit.deployment.git import get_current_branch
from lab_toolkit.deployment.pipeline import apply_config

CURRENT_CONFIG_REMOTE_DIR = "/var/www/labs/test-project"

CURRENT_CONFIG = {
    DEPLOYMENT.REMOTE_DIR: "/var/www/labs/test-project",
    DEPLOYMENT.BASE: "/",
    "description": "Configuration de test",
    "environment": "development",
}

EXPECTED_REMOTE_DIR = "/var/www/labs/lab-front-react"

PROPOSED_CONFIG = {
    DEPLOYMENT.REMOTE_DIR: f"{EXPECTED_REMOTE_DIR}/{BRANCH.SOCLE}",
    DEPLOYMENT.BASE: "/",
}


def test_apply_config_pipeline_saves_configuration(monkeypatch):
    # prepare
    saved_configs = []
    monkeypatch.setattr(
        apply_config,
        get_current_branch.__name__,
        lambda: BRANCH.SOCLE,
    )
    monkeypatch.setattr(
        apply_config,
        load_config.__name__,
        lambda: CURRENT_CONFIG,
    )
    monkeypatch.setattr(
        apply_config,
        build_deployment_config.__name__,
        lambda: PROPOSED_CONFIG,
    )
    monkeypatch.setattr(
        apply_config,
        save_config.__name__,
        lambda config: saved_configs.append(config),
    )

    # execute
    result = apply_config.apply_config_pipeline()

    # tests
    assert saved_configs == [
        {
            **CURRENT_CONFIG,
            **PROPOSED_CONFIG,
        }
    ]

    assert result == {
        "branch": BRANCH.SOCLE,
        DEPLOYMENT.REMOTE_DIR: f"{EXPECTED_REMOTE_DIR}/{BRANCH.SOCLE}",
        DEPLOYMENT.BASE: "/",
    }


def test_apply_config_pipeline_preserves_additional_fields(monkeypatch):
    # prepare
    saved_configs = []
    monkeypatch.setattr(
        apply_config,
        get_current_branch.__name__,
        lambda: BRANCH.SOCLE,
    )
    monkeypatch.setattr(
        apply_config,
        load_config.__name__,
        lambda: CURRENT_CONFIG,
    )
    monkeypatch.setattr(
        apply_config,
        build_deployment_config.__name__,
        lambda: PROPOSED_CONFIG,
    )
    monkeypatch.setattr(
        apply_config,
        save_config.__name__,
        lambda config: saved_configs.append(config),
    )

    # execute
    apply_config.apply_config_pipeline()

    # tests
    saved_config = saved_configs[0]

    assert saved_config["description"] == "Configuration de test"
    assert saved_config["environment"] == "development"


def test_apply_config_pipeline_returns_updated_configuration(monkeypatch):
    # prepare
    saved_configs = []
    monkeypatch.setattr(
        apply_config,
        get_current_branch.__name__,
        lambda: BRANCH.SOCLE,
    )
    monkeypatch.setattr(
        apply_config,
        load_config.__name__,
        lambda: CURRENT_CONFIG,
    )
    monkeypatch.setattr(
        apply_config,
        build_deployment_config.__name__,
        lambda: PROPOSED_CONFIG,
    )
    monkeypatch.setattr(
        apply_config,
        save_config.__name__,
        lambda config: saved_configs.append(config),
    )

    # execute
    result = apply_config.apply_config_pipeline()
    # tests
    assert isinstance(result, dict)
