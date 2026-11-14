from dataclasses import dataclass


@dataclass(frozen=True)
class BrancheConstants:
    """Constantes associées aux branches Git authorisées."""

    SOCLE: str = "socle"
    EXPERIENCE_PREFIX: str = "experience/"


BRANCH = BrancheConstants()
