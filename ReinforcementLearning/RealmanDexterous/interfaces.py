from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class RobotObservation:
    arm_joint: List[float]
    hand_joint: List[float]
    tactile: List[float]
    wrench: List[float]
    extras: Dict[str, float]


class ArmDriver(ABC):
    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_joint(self) -> List[float]:
        raise NotImplementedError

    @abstractmethod
    def command_joint(self, target: List[float]) -> None:
        raise NotImplementedError


class HandDriver(ABC):
    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_joint(self) -> List[float]:
        raise NotImplementedError

    @abstractmethod
    def command_joint(self, target: List[float]) -> None:
        raise NotImplementedError


class TactileDriver(ABC):
    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def read(self) -> List[float]:
        raise NotImplementedError
