from lab_toolkit.deployment.pipeline import apply_config

CURRENT_CONFIG = {
    "remoteDir": "/var/www/labs/test-project",
    "base": "/",
    "description": "Configuration de test",
    "environment": "development",
}

PROPOSED_CONFIG = {
    "remoteDir": "/var/www/labs/lab-front-react/socle",
    "base": "/",
}


def test_apply_config_pipeline_saves_configuration(
    monkeypatch,
    capsys,
):
    saved_configs = []

    monkeypatch.setattr(
        apply_config,
        "load_config",
        lambda: CURRENT_CONFIG,
    )
    monkeypatch.setattr(
        apply_config,
        "build_deployment_config",
        lambda: PROPOSED_CONFIG,
    )
    monkeypatch.setattr(
        apply_config,
        "save_config",
        lambda config: saved_configs.append(config),
    )

    apply_config.apply_config_pipeline()

    output = capsys.readouterr().out

    assert saved_configs == [
        {
            **CURRENT_CONFIG,
            **PROPOSED_CONFIG,
        }
    ]

    assert "remoteDir : /var/www/labs/lab-front-react/socle" in output
    assert "base      : /" in output


def test_apply_config_pipeline_preserves_additional_fields(
    monkeypatch,
):
    saved_configs = []

    monkeypatch.setattr(
        apply_config,
        "load_config",
        lambda: CURRENT_CONFIG,
    )
    monkeypatch.setattr(
        apply_config,
        "build_deployment_config",
        lambda: PROPOSED_CONFIG,
    )
    monkeypatch.setattr(
        apply_config,
        "save_config",
        lambda config: saved_configs.append(config),
    )

    apply_config.apply_config_pipeline()

    saved_config = saved_configs[0]

    assert saved_config["description"] == "Configuration de test"
    assert saved_config["environment"] == "development"
