from ..config import LogConfig, PipelineStep
from .base import BaseFormatter


class TreeFormatter(BaseFormatter):
    """Affichage hiérarchique des appels de fonctions."""

    def format(
        self,
        level: str,
        config: LogConfig,
        use_color: bool,
    ) -> str:
        lines = self.format_header(config, use_color)

        lines.append(self.format_status(level, config, use_color))

        if config.steps:
            steps_by_parent: dict[
                int | None,
                list[tuple[int, PipelineStep]],
            ] = {}

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
        node_index: int,
        step: PipelineStep,
        steps_by_parent: dict[
            int | None,
            list[tuple[int, PipelineStep]],
        ],
        lines: list[str],
        use_color: bool,
        prefix: str,
        is_last: bool,
    ) -> None:
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
