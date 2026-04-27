from dataclasses import dataclass, field

from lerobot.cameras import CameraConfig
from lerobot.cameras.opencv import OpenCVCameraConfig
from lerobot.robots import RobotConfig

DEFAULT_FOLLOWER_IDS = {
    "joint_1": 11,
    "joint_2": 12,
    "joint_3": 13,
    "joint_4": 14,
    "gripper": 15,
}


def _default_cameras() -> dict[str, CameraConfig]:
    return {
        "front": OpenCVCameraConfig(
            index_or_path=0,
            fps=30,
            width=320,
            height=240,
        ),
        "around": OpenCVCameraConfig(
            index_or_path=1,
            fps=30,
            width=320,
            height=240,
        ),
    }


@RobotConfig.register_subclass("openmanipulator_x_follower")
@dataclass(kw_only=True)
class OpenManipulatorXFollowerConfig(RobotConfig):
    port: str
    joint_ids: dict[str, int] = field(default_factory=lambda: DEFAULT_FOLLOWER_IDS.copy())
    cameras: dict[str, CameraConfig] = field(default_factory=_default_cameras)
    disable_torque_on_disconnect: bool = True
    use_joint_degrees: bool = True
    drive_mode: dict[str, int] = field(default_factory=dict)
