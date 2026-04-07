from dataclasses import dataclass, field
from typing import List


@dataclass
class RealmanConfig:
    host: str = "192.168.1.18"
    port: int = 8080
    control_hz: int = 100
    arm_dof: int = 6
    max_joint_velocity: float = 0.5
    max_joint_step: float = 0.02
    home_joint: List[float] = field(default_factory=lambda: [0.0, -0.3, 0.5, 0.0, 1.57, 0.0])


@dataclass
class InshiHandConfig:
    port: str = "/dev/ttyUSB0"
    baudrate: int = 115200
    hand_dof: int = 12
    max_joint_step: float = 0.03
    startup_joint: List[float] = field(default_factory=lambda: [0.2] * 12)


@dataclass
class PolicyConfig:
    checkpoint_path: str = "./checkpoints/policy.pt"
    obs_dim: int = 96
    action_dim: int = 18
    device: str = "cpu"
    action_scale: float = 1.0
    use_tanh: bool = True


@dataclass
class SafetyConfig:
    emergency_stop_force: float = 30.0
    emergency_stop_torque: float = 2.0
    command_timeout_sec: float = 0.2


@dataclass
class DeployConfig:
    realman: RealmanConfig = field(default_factory=RealmanConfig)
    hand: InshiHandConfig = field(default_factory=InshiHandConfig)
    policy: PolicyConfig = field(default_factory=PolicyConfig)
    safety: SafetyConfig = field(default_factory=SafetyConfig)
