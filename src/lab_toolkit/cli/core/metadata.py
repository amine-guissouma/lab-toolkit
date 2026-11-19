from importlib.metadata import PackageNotFoundError, metadata, version


def get_project_metadata(distribution_name: str) -> dict[str, str]:
    """Récupère les métadonnées d'un package installé."""

    try:
        project_metadata = metadata(distribution_name)

        return {
            "name": project_metadata.get("Name", distribution_name),
            "version": version(distribution_name),
            "description": project_metadata.get(
                "Summary",
                "Aucune description disponible.",
            ),
        }

    except PackageNotFoundError as exc:
        raise RuntimeError(
            f"Impossible de récupérer les métadonnées de "
            f"'{distribution_name}'. "
            "Installe le projet avec 'pip install -e .'."
        ) from exc
