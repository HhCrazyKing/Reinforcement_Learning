from __future__ import annotations

import csv
import time
from pathlib import Path

from config import DeployConfig
from inshi_hand_api import InshiSerialHandDriver
from realman_api import RealmanHttpDriver


def main() -> None:
    cfg = DeployConfig()
    arm = RealmanHttpDriver(cfg.realman)
    hand = InshiSerialHandDriver(cfg.hand)
    arm.connect()
    hand.connect()

    out_dir = Path("./dataset")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"realman_inshi_{int(time.time())}.csv"

    with out_file.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ts", "arm_joint", "hand_joint"])
        while True:
            ts = time.time()
            writer.writerow([ts, arm.get_joint(), hand.get_joint()])
            f.flush()
            time.sleep(0.02)


if __name__ == "__main__":
    main()
