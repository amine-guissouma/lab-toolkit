from ..config import LogConfig
from .base import BaseFormatter


class PipelineFormatter(BaseFormatter):
    """Affichage chronologique des appels de fonctions."""

    def format(
        self,
        level: str,
        config: LogConfig,
        use_color: bool,
    ) -> str:
        lines = self.format_header(config, use_color)

        lines.append(self.format_status(level, config, use_color))

        for index, step in enumerate(config.steps):
            prefix = "      " if index == 0 else "      |"

            lines.append(self.colorize(prefix, self.style.purple, use_color))

            lines.append(self.format_step_status(step, use_color))

            lines.extend(self.format_step_error(step, use_color))

        if config.error_message and not any(step.error for step in config.steps):
            lines.append(
                self.colorize(
                    f"         └─-→ {config.error_message}",
                    self.style.error.color,
                    use_color,
                )
            )

        if config.details:
            lines.extend(self.format_details(config.details, use_color))

        lines.extend(self.format_footer(use_color))

        return "\n".join(lines)
