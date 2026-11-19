import os
import sys
from typing import TextIO

from lab_toolkit.logger.config import LogConfig
from lab_toolkit.logger.formatters import LogFormatter
from lab_toolkit.logger.styling.styles import LogStyle


class Logger:
    def __init__(
        self,
        style: LogStyle | None = None,
        use_color: bool | None = None,
    ):
        self.style = style or LogStyle()
        self.formatter = LogFormatter(self.style)
        self.use_color = use_color

    def _get_stream(self, level: str) -> TextIO:
        if level in ("ERROR", "WARNING"):
            return sys.stderr

        return sys.stdout

    def _colors_enabled(self, stream: TextIO) -> bool:
        if self.use_color is not None:
            return self.use_color

        if os.getenv("NO_COLOR") is not None:
            return False

        if os.getenv("TERM") == "dumb":
            return False

        return stream.isatty()

    def _log(self, level: str, config: LogConfig) -> None:
        stream = self._get_stream(level)

        message = self.formatter.format(
            level=level,
            config=config,
            use_color=self._colors_enabled(stream),
        )

        stream.write(message + "\n")
        stream.flush()

    def success(self, config: LogConfig) -> None:
        self._log("SUCCESS", config)

    def error(self, config: LogConfig) -> None:
        self._log("ERROR", config)

    def warning(self, config: LogConfig) -> None:
        self._log("WARNING", config)

    def info(self, config: LogConfig) -> None:
        self._log("INFO", config)

    def debug(self, config: LogConfig) -> None:
        self._log("DEBUG", config)


# Instance réutilisable dans tout le projet
log = Logger()
