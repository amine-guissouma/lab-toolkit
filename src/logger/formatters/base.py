from collections.abc import Mapping
from datetime import datetime
from pathlib import Path

from ..config import LogConfig, PipelineStep
from ..styling.styles import LogStyle


class BaseFormatter:
    """Fonctions communes aux différents formats d'affichage."""

    def __init__(self, style: LogStyle | None = None):
        self.style = style or LogStyle()

    def colorize(self, text: str, color: str, enabled: bool) -> str:
        if not enabled:
            return text

        return f"{color}{text}{self.style.reset}"

    def format_header(self, config: LogConfig, use_color: bool) -> list[str]:
        timestamp = config.timestamp or datetime.now()
        timestamp_text = timestamp.strftime("%Y-%m-%d_%H-%M-%S")

        laboratory = config.project or Path.cwd().name

        header = f"─-→ {laboratory} -─────────────-→ {timestamp_text}-"

        return [
            self.colorize(header, self.style.header_color, use_color),
            self.colorize(
                "    -──────────-",
                self.style.header_color,
                use_color,
            ),
        ]

    def format_status(
        self,
        level: str,
        config: LogConfig,
        use_color: bool,
    ) -> str:
        level = level.upper()
        level_style = self.style.get_level_style(level)

        status = self.colorize(
            f"[{level}]",
            level_style.color + self.style.bold,
            use_color,
        )

        action = self.colorize(
            config.action,
            level_style.color,
            use_color,
        )

        return f"{status} {level_style.icon}  {action} ── {config.target}"

    def format_details(
        self,
        details: Mapping[str, object],
        use_color: bool,
    ) -> list[str]:
        lines = []
        items = list(details.items())

        for index, (key, value) in enumerate(items):
            connector = "└──" if index == len(items) - 1 else "├──"
            label = f"      {connector} {key} :"

            lines.append(
                f"{self.colorize(label, self.style.purple, use_color)} {value}"
            )

        return lines

    def format_footer(self, use_color: bool) -> list[str]:
        return [
            "",
            self.colorize(
                "←-───────────────────────────────────────────────-→",
                self.style.footer_color,
                use_color,
            ),
        ]

    def format_step_status(
        self,
        step: PipelineStep,
        use_color: bool,
    ) -> str:
        if step.success:
            message = f"    ✅ SUCCESS → {step.name}"
            return self.colorize(
                message,
                self.style.success.color,
                use_color,
            )

        message = f"    ❌ ERROR x {step.name}"
        return self.colorize(
            message,
            self.style.error.color,
            use_color,
        )

    def format_step_error(
        self,
        step: PipelineStep,
        use_color: bool,
        prefix: str = "          └─-→ ",
    ) -> list[str]:
        if not step.error:
            return []

        return [
            self.colorize(
                f"{prefix}{line}",
                self.style.error.color,
                use_color,
            )
            for line in step.error.splitlines()
        ]
