from ..config import LogConfig
from ..exceptions import LogConfigurationError
from ..styling.styles import LogStyle
from .base import BaseFormatter
from .pipeline import PipelineFormatter
from .simple import SimpleFormatter
from .tree import TreeFormatter


class LogFormatter:
    """Sélectionne le formateur selon le mode demandé."""

    def __init__(self, style: LogStyle | None = None):
        self.style = style or LogStyle()

        self.formatters: dict[str, BaseFormatter] = {
            "simple": SimpleFormatter(self.style),
            "pipeline": PipelineFormatter(self.style),
            "tree": TreeFormatter(self.style),
        }

    def format(
        self,
        level: str,
        config: LogConfig,
        use_color: bool = True,
    ) -> str:
        mode = config.display_mode

        try:
            formatter = self.formatters[mode]
        except KeyError:
            raise LogConfigurationError(f"Mode d'affichage inconnu : {mode}") from None

        return formatter.format(level, config, use_color)
