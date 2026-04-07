from __future__ import annotations

from typing import List

import numpy as np
import torch

from config import PolicyConfig


class TactileDexterityPolicy:
    """
    加载 tactile-dexterity 导出的 torchscript/pytorch policy。
    输入必须与训练时 observation 拼接顺序一致。
    """

    def __init__(self, cfg: PolicyConfig):
        self.cfg = cfg
        self.device = torch.device(cfg.device)
        self.model = torch.jit.load(cfg.checkpoint_path, map_location=self.device)
        self.model.eval()

    def act(self, obs: List[float]) -> List[float]:
        if len(obs) != self.cfg.obs_dim:
            raise ValueError(f"obs dim mismatch: got {len(obs)}, expect {self.cfg.obs_dim}")
        tensor = torch.tensor(np.array(obs), dtype=torch.float32, device=self.device).unsqueeze(0)
        with torch.no_grad():
            action = self.model(tensor)[0].detach().cpu().numpy()
        if self.cfg.use_tanh:
            action = np.tanh(action)
        action = (action * self.cfg.action_scale).tolist()
        if len(action) != self.cfg.action_dim:
            raise ValueError(f"action dim mismatch: got {len(action)}, expect {self.cfg.action_dim}")
        return action
