from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class PipelineStep:
    name: str
    success: bool
    error: str | None = None
    parent_id: int | None = None


@dataclass(frozen=True)
class LogConfig:
    project: str
    action: str
    target: str
    details: Mapping[str, object] = field(default_factory=dict)
    steps: tuple[PipelineStep, ...] = ()
    timestamp: datetime | None = None
    display_mode: str = "pipeline"
    error_message: str | None = None
