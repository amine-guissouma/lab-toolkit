from dataclasses import dataclass, field


@dataclass(frozen=True)
class LogLevelStyle:
    color: str
    icon: str


@dataclass(frozen=True)
class LogStyle:
    reset: str = "\033[0m"
    bold: str = "\033[1m"

    success: LogLevelStyle = field(
        default_factory=lambda: LogLevelStyle(
            color="\033[32m",
            icon="✅",
        )
    )

    error: LogLevelStyle = field(
        default_factory=lambda: LogLevelStyle(
            color="\033[31m",
            icon="❌",
        )
    )

    warning: LogLevelStyle = field(
        default_factory=lambda: LogLevelStyle(
            color="\033[33m",
            icon="⚠️",
        )
    )

    info: LogLevelStyle = field(
        default_factory=lambda: LogLevelStyle(
            color="\033[34m",
            icon="ℹ️",
        )
    )

    debug: LogLevelStyle = field(
        default_factory=lambda: LogLevelStyle(
            color="\033[90m",
            icon="🔍",
        )
    )

    header_color: str = "\033[36m"
    footer_color: str = "\033[36m"
    purple: str = "\033[35m"

    def get_level_style(self, level: str) -> LogLevelStyle:
        styles = {
            "SUCCESS": self.success,
            "ERROR": self.error,
            "WARNING": self.warning,
            "INFO": self.info,
            "DEBUG": self.debug,
        }

        try:
            return styles[level.upper()]
        except KeyError:
            raise ValueError(f"Niveau de log inconnu : {level}") from None
