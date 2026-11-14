from dataclasses import dataclass, field
from typing import Any
from unittest.mock import Mock

from _pytest.monkeypatch import MonkeyPatch


@dataclass
class MockConfig:
    name: str
    return_value: Any = None
    side_effect: Any = None
    expected_calls: int = 1
    expected_args: tuple = field(default_factory=tuple)
    expected_kwargs: dict = field(default_factory=dict)

    mock: Mock = field(init=False)

    def __post_init__(self):
        self.mock = Mock(
            return_value=self.return_value,
            side_effect=self.side_effect,
        )


def mocks_function(function, mocks: list[MockConfig], monkeypatch: MonkeyPatch):
    for config in mocks:
        monkeypatch.setattr(
            function,
            config.name,
            config.mock,
        )


def assert_mock(mocks: list[MockConfig]):
    for config in mocks:
        if config.expected_calls == 1:
            config.mock.assert_called_once()
        elif config.expected_args == tuple():
            config.mock.assert_called_once_with(config.expected_calls)
