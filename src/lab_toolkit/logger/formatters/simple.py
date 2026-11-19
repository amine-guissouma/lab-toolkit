from ..config import LogConfig
from .base import BaseFormatter


class SimpleFormatter(BaseFormatter):
    """Affichage synthétique du résultat."""

    def format(
        self,
        level: str,
        config: LogConfig,
        use_color: bool,
    ) -> str:
        lines = self.format_header(config, use_color)

        lines.append(self.format_status(level, config, use_color))

        root = config.steps[0] if config.steps else None

        if root:
            if root.success:
                message = f"✅ {root.name}"
                lines.append(
                    self.colorize(message, self.style.success.color, use_color)
                )
            else:
                message = f"❌ {root.name}"
                lines.append(self.colorize(message, self.style.error.color, use_color))

        if config.error_message:
            for error_line in config.error_message.splitlines():
                lines.append(
                    self.colorize(
                        f"    └─-→  {error_line}",
                        self.style.error.color,
                        use_color,
                    )
                )

        if config.details:
            lines.extend(self.format_details(config.details, use_color))

        lines.extend(self.format_footer(use_color))

        return "\n".join(lines)
