from __future__ import annotations

import time
from typing import List

import numpy as np

from config import DeployConfig
from inshi_hand_api import InshiSerialHandDriver
from realman_api import RealmanHttpDriver
from tactile_policy_runner import TactileDexterityPolicy


def clip_step(target: List[float], current: List[float], max_step: float) -> List[float]:
    delta = np.array(target) - np.array(current)
    delta = np.clip(delta, -max_step, max_step)
    return (np.array(current) + delta).tolist()


def safe_guard(wrench: List[float], max_force: float, max_torque: float) -> bool:
    force = np.linalg.norm(wrench[:3])
    torque = np.linalg.norm(wrench[3:6])
    return force < max_force and torque < max_torque


def build_obs(arm_joint: List[float], hand_joint: List[float], tactile: List[float], wrench: List[float]) -> List[float]:
    return arm_joint + hand_joint + tactile + wrench


def main() -> None:
    cfg = DeployConfig()
    arm = RealmanHttpDriver(cfg.realman)
    hand = InshiSerialHandDriver(cfg.hand)
    policy = TactileDexterityPolicy(cfg.policy)

    arm.connect()
    hand.connect()

    arm.command_joint(cfg.realman.home_joint)
    hand.command_joint(cfg.hand.startup_joint)

    period = 1.0 / cfg.realman.control_hz
    last_policy_time = time.time()

    while True:
        now = time.time()
        arm_joint = arm.get_joint()
        hand_joint = hand.get_joint()

        # 将 tactile / wrench 改为你实际传感器接口读取
        tactile = [0.0] * (cfg.policy.obs_dim - cfg.realman.arm_dof - cfg.hand.hand_dof - 6)
        wrench = [0.0] * 6

        if not safe_guard(wrench, cfg.safety.emergency_stop_force, cfg.safety.emergency_stop_torque):
            print("[E-STOP] force/torque exceeded, stopping loop")
            break

        if now - last_policy_time > cfg.safety.command_timeout_sec:
            print("[TIMEOUT] policy cycle timeout")
            break

        obs = build_obs(arm_joint, hand_joint, tactile, wrench)
        action = policy.act(obs)

        arm_target = clip_step(
            [a + b for a, b in zip(arm_joint, action[: cfg.realman.arm_dof])],
            arm_joint,
            cfg.realman.max_joint_step,
        )
        hand_target = clip_step(
            [a + b for a, b in zip(hand_joint, action[cfg.realman.arm_dof :])],
            hand_joint,
            cfg.hand.max_joint_step,
        )

        arm.command_joint(arm_target)
        hand.command_joint(hand_target)
        last_policy_time = now
        time.sleep(period)


if __name__ == "__main__":
    main()
