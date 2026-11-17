from datetime import datetime
from pathlib import Path

from lab_toolkit.logger.config import LogConfig
from lab_toolkit.logger.styles import LogStyle


class LogFormatter:
    def __init__(self, style: LogStyle | None = None):
        self.style = style or LogStyle()

    def _colorize(
        self,
        text: str,
        color: str,
        enabled: bool,
    ) -> str:
        if not enabled:
            return text

        return f"{color}{text}{self.style.reset}"

    def format(
        self,
        level: str,
        config: LogConfig,
        use_color: bool = True,
    ) -> str:
        level = level.upper()
        level_style = self.style.get_level_style(level)

        timestamp = config.timestamp or datetime.now()
        timestamp_text = timestamp.strftime("%Y-%m-%d_%H-%M-%S")

        laboratory = config.project or Path.cwd().name

        lines = []

        # Header
        header = f"─-→ {laboratory} -─────────────-→ {timestamp_text}-"

        lines.append(
            self._colorize(
                header,
                self.style.header_color,
                use_color,
            )
        )

        lines.append(
            self._colorize(
                "    -──────────-",
                self.style.header_color,
                use_color,
            )
        )

        # Status
        status = self._colorize(
            f"[{level}]",
            level_style.color + self.style.bold,
            use_color,
        )

        action = self._colorize(
            config.action,
            level_style.color,
            use_color,
        )

        lines.append(f"{status} {level_style.icon}  {action} ── {config.target}")

        # Details
        lines.extend(self._format_steps(config.steps, use_color))

        if config.details:
            if config.steps:
                lines.append("")

            lines.extend(self._format_details(config.details, use_color))

        # Footer
        lines.append("")

        lines.append(
            self._colorize(
                "←-───────────────────────────────────────────────-→",
                self.style.footer_color,
                use_color,
            )
        )

        return "\n".join(lines)

    def _format_steps(self, steps, use_color):
        lines = []

        for step in steps:
            lines.append(self._colorize("      |", self.style.purple, use_color))

            if step.success:
                message = f"    ✅ SUCCESS → {step.name}"
                lines.append(
                    self._colorize(message, self.style.success.color, use_color)
                )
            else:
                message = f"    ❌ ERROR x {step.name}"
                lines.append(self._colorize(message, self.style.error.color, use_color))

                if step.error:
                    for error_line in step.error.splitlines():
                        lines.append(
                            self._colorize(
                                f"          └─-→ {error_line}",
                                self.style.error.color,
                                use_color,
                            )
                        )

        return lines

    def _format_details(self, details, use_color):
        lines = []
        items = list(details.items())

        for index, (key, value) in enumerate(items):
            connector = "└──" if index == len(items) - 1 else "├──"
            label = f"      {connector} {key} :"

            lines.append(
                f"{self._colorize(label, self.style.purple, use_color)} {value}"
            )

        return lines
