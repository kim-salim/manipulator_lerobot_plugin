from dataclasses import dataclass, field

from lerobot.teleoperators.config import TeleoperatorConfig

DEFAULT_LEADER_IDS = {
    "joint_1": 11,
    "joint_2": 12,
    "joint_3": 13,
    "joint_4": 14,
    "gripper": 15,
}


@TeleoperatorConfig.register_subclass("openmanipulator_x_leader")
@dataclass(kw_only=True)
class OpenManipulatorXLeaderConfig(TeleoperatorConfig):
    port: str
    joint_ids: dict[str, int] = field(default_factory=lambda: DEFAULT_LEADER_IDS.copy())
    disable_torque_on_disconnect: bool = True
    use_joint_degrees: bool = True
    drive_mode: dict[str, int] = field(default_factory=dict)
