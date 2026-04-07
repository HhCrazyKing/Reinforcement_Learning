# Realman + 因时灵巧手部署桥接（对接 tactile-dexterity）

这个目录把 `tactile-dexterity` 的策略推理流程改造成可直接落地到 **Realman 机械臂 + 因时灵巧手** 的在线控制框架。

> 说明：由于硬件 SDK 版本和现场网络/总线配置差异较大，这里提供的是**可直接运行的部署骨架**，你只需要替换两个 driver 的底层报文即可上线。

## 目录说明

- `config.py`：硬件地址、DOF、控制频率、安全阈值、policy 参数。
- `realman_api.py`：Realman HTTP 控制驱动（启停、读状态、发关节命令）。
- `inshi_hand_api.py`：因时灵巧手串口驱动（可替换为厂家 SDK binding）。
- `tactile_policy_runner.py`：加载 tactile-dexterity 导出的 TorchScript 策略。
- `deploy.py`：主控制环，执行观测拼接、安全检查、动作限幅、下发控制。
- `teleop_collect.py`：示教/回放前的数据采集模板。

## 如何对接 tactile-dexterity

1. 在 tactile-dexterity 工程中导出策略为 TorchScript（`policy.pt`）。
2. 把导出的模型放到本目录 `./checkpoints/policy.pt`（或改 `PolicyConfig.checkpoint_path`）。
3. 确保 `PolicyConfig.obs_dim/action_dim` 和训练时完全一致。
4. 把 `deploy.py` 中 `tactile` 与 `wrench` 的占位读取改为你的传感器实际接口。
5. 根据现场限位与安全策略，调整 `max_joint_step`、急停阈值。

## 运行

```bash
cd ReinforcementLearning/RealmanDexterous
python -m pip install -r requirements.txt
python deploy.py
```

## 真实落地建议

- 首次上机先把 `action_scale` 调小（如 `0.1`），验证方向正确再放开。
- 先只开机械臂 DOF（手固定），再逐步放开手指关节。
- 建议把 `safe_guard` 接入真实六维力和碰撞检测信号。
- 建议在工控机上启用独立 watchdog，在控制进程异常退出时回到 home。
