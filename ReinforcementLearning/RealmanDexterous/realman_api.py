from __future__ import annotations

import requests
from typing import List

from config import RealmanConfig
from interfaces import ArmDriver


class RealmanHttpDriver(ArmDriver):
    """
    适配 Realman 机械臂 HTTP 控制接口。
    若你的固件接口字段不同，仅需修改 _post 的 payload。
    """

    def __init__(self, cfg: RealmanConfig):
        self.cfg = cfg
        self.base = f"http://{cfg.host}:{cfg.port}"

    def _post(self, path: str, payload: dict) -> dict:
        r = requests.post(f"{self.base}{path}", json=payload, timeout=0.1)
        r.raise_for_status()
        return r.json()

    def connect(self) -> None:
        self._post("/api/enable", {"enable": True})

    def get_joint(self) -> List[float]:
        data = self._post("/api/state", {})
        return data.get("joint", [0.0] * self.cfg.arm_dof)

    def command_joint(self, target: List[float]) -> None:
        self._post(
            "/api/joint_command",
            {
                "joint": target,
                "vel": self.cfg.max_joint_velocity,
            },
        )
