from __future__ import annotations

from typing import List

import serial

from config import InshiHandConfig
from interfaces import HandDriver


class InshiSerialHandDriver(HandDriver):
    """
    因时灵巧手串口驱动示例。
    实际部署时建议替换为厂商 SDK 的 Python binding。
    """

    def __init__(self, cfg: InshiHandConfig):
        self.cfg = cfg
        self.ser: serial.Serial | None = None

    def connect(self) -> None:
        self.ser = serial.Serial(self.cfg.port, self.cfg.baudrate, timeout=0.01)

    def get_joint(self) -> List[float]:
        if self.ser is None:
            return [0.0] * self.cfg.hand_dof
        self.ser.write(b"GET_JOINT\n")
        line = self.ser.readline().decode().strip()
        if not line:
            return [0.0] * self.cfg.hand_dof
        values = [float(v) for v in line.split(",")]
        return values[: self.cfg.hand_dof]

    def command_joint(self, target: List[float]) -> None:
        if self.ser is None:
            raise RuntimeError("serial not connected")
        cmd = "SET_JOINT," + ",".join(f"{v:.4f}" for v in target) + "\n"
        self.ser.write(cmd.encode())
