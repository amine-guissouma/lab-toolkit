from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class PipelineStep:
    name: str
    success: bool
    error: str | None = None


@dataclass(frozen=True)
class LogConfig:
    project: str
    action: str
    target: str
    details: Mapping[str, object] = field(default_factory=dict)
    steps: tuple[PipelineStep, ...] = ()
    timestamp: datetime | None = None
