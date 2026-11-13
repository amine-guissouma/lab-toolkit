from lab_toolkit.deployment.pipeline import show_config_pipeline

CURRENT_CONFIG = {
    "remoteDir": "/var/www/labs/test-project",
    "base": "/",
    "description": "Configuration de test",
}

PROPOSED_CONFIG = {
    "remoteDir": "/var/www/labs/lab-front-react/socle",
    "base": "/",
}


def test_show_config_pipeline_displays_configuration(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        show_config_pipeline,
        "load_config",
        lambda: CURRENT_CONFIG,
    )
    monkeypatch.setattr(
        show_config_pipeline,
        "build_deployment_config",
        lambda: PROPOSED_CONFIG,
    )

    show_config_pipeline.show_config_pipeline()

    output = capsys.readouterr().out

    assert "Configuration actuelle :" in output
    assert "Configuration proposée :" in output

    assert "/var/www/labs/test-project" in output
    assert "/var/www/labs/lab-front-react/socle" in output

    assert "Aucune modification effectuée." in output


def test_show_config_pipeline_does_not_modify_current_config(
    monkeypatch,
):
    original_config = CURRENT_CONFIG.copy()

    monkeypatch.setattr(
        show_config_pipeline,
        "load_config",
        lambda: CURRENT_CONFIG,
    )
    monkeypatch.setattr(
        show_config_pipeline,
        "build_deployment_config",
        lambda: PROPOSED_CONFIG,
    )

    show_config_pipeline.show_config_pipeline()

    assert original_config == CURRENT_CONFIG
