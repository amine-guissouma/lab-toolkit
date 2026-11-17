from datetime import datetime
from pathlib import Path

from .config import LogConfig, PipelineStep
from .exceptions import LogConfigurationError
from .styles import LogStyle


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

    def format_status(self, level: str, config: LogConfig, use_color: bool) -> str:
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

    def format_details(self, details, use_color: bool) -> list[str]:
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


class SimpleFormatter(BaseFormatter):
    """Affichage synthétique du résultat."""

    def format(self, level: str, config: LogConfig, use_color: bool) -> str:
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


class PipelineFormatter(BaseFormatter):
    """Affichage chronologique des appels de fonctions."""

    def format(self, level: str, config: LogConfig, use_color: bool) -> str:
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


class TreeFormatter(BaseFormatter):
    """Affichage hiérarchique des appels de fonctions."""

    def format(self, level: str, config: LogConfig, use_color: bool) -> str:
        lines = self.format_header(config, use_color)

        lines.append(self.format_status(level, config, use_color))

        if config.steps:
            steps_by_parent: dict[int | None, list[tuple[int, PipelineStep]]] = {}

            for index, step in enumerate(config.steps):
                steps_by_parent.setdefault(step.parent_id, []).append((index, step))

            roots = steps_by_parent.get(None, [])

            for root_index, root in roots:
                self._format_node(
                    root_index,
                    root,
                    steps_by_parent,
                    lines,
                    use_color,
                    prefix="",
                    is_last=True,
                )

        if config.error_message and not any(step.error for step in config.steps):
            lines.append(
                self.colorize(
                    f"    └─-→ {config.error_message}",
                    self.style.error.color,
                    use_color,
                )
            )

        if config.details:
            lines.append("")
            lines.extend(self.format_details(config.details, use_color))

        lines.extend(self.format_footer(use_color))

        return "\n".join(lines)

    def _format_node(
        self,
        node_index,
        step,
        steps_by_parent,
        lines,
        use_color,
        prefix,
        is_last,
    ):
        if prefix:
            connector = "└→ " if is_last else "├→ "
            continuation = "    " if is_last else "│   "
        else:
            connector = ""
            continuation = "    "

        if step.success:
            message = f"{connector}✅ {step.name}"
            color = self.style.success.color
        else:
            message = f"{connector}❌ {step.name}"
            color = self.style.error.color

        lines.append(
            self.colorize(
                f"{prefix}{message}",
                color,
                use_color,
            )
        )

        if step.error:
            for error_line in step.error.splitlines():
                lines.append(
                    self.colorize(
                        f"{prefix}{continuation}└→ {error_line}",
                        self.style.error.color,
                        use_color,
                    )
                )

        children = steps_by_parent.get(node_index, [])

        for child_position, (child_index, child) in enumerate(children):
            child_is_last = child_position == len(children) - 1

            self._format_node(
                child_index,
                child,
                steps_by_parent,
                lines,
                use_color,
                prefix=f"{prefix}{continuation}",
                is_last=child_is_last,
            )


class LogFormatter:
    """Sélectionne le formateur selon le mode demandé."""

    def __init__(self, style: LogStyle | None = None):
        self.style = style or LogStyle()

        self.formatters = {
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
