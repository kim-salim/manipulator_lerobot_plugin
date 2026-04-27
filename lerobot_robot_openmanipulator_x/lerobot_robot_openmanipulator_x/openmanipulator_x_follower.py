from __future__ import annotations

from typing import Any

from lerobot.cameras import make_cameras_from_configs
from lerobot.motors import Motor, MotorCalibration, MotorNormMode
from lerobot.motors.dynamixel import DynamixelMotorsBus, OperatingMode
from lerobot.robots import Robot

from .config_openmanipulator_x_follower import OpenManipulatorXFollowerConfig


class OpenManipulatorXFollower(Robot):
    config_class = OpenManipulatorXFollowerConfig
    name = "openmanipulator_x_follower"

    ARM_JOINTS = ("joint_1", "joint_2", "joint_3", "joint_4")
    ALL_JOINTS = ARM_JOINTS + ("gripper",)
    MOTOR_MODEL = "xm430-w350"

    def __init__(self, config: OpenManipulatorXFollowerConfig):
        super().__init__(config)
        self.config = config

        joint_norm_mode = (
            MotorNormMode.DEGREES if config.use_joint_degrees else MotorNormMode.RANGE_M100_100
        )

        motors = {
            "joint_1": Motor(config.joint_ids["joint_1"], self.MOTOR_MODEL, joint_norm_mode),
            "joint_2": Motor(config.joint_ids["joint_2"], self.MOTOR_MODEL, joint_norm_mode),
            "joint_3": Motor(config.joint_ids["joint_3"], self.MOTOR_MODEL, joint_norm_mode),
            "joint_4": Motor(config.joint_ids["joint_4"], self.MOTOR_MODEL, joint_norm_mode),
            "gripper": Motor(config.joint_ids["gripper"], self.MOTOR_MODEL, MotorNormMode.RANGE_0_100),
        }

        self.bus = DynamixelMotorsBus(
            port=config.port,
            motors=motors,
            calibration=self.calibration,
        )
        self.cameras = make_cameras_from_configs(config.cameras)

    @property
    def _motors_ft(self) -> dict[str, type]:
        return {f"{motor}.pos": float for motor in self.ALL_JOINTS}

    @property
    def _cameras_ft(self) -> dict[str, tuple[int, int, int]]:
        return {
            cam_name: (camera.height, camera.width, 3)
            for cam_name, camera in self.cameras.items()
        }

    @property
    def observation_features(self) -> dict:
        return {**self._motors_ft, **self._cameras_ft}

    @property
    def action_features(self) -> dict:
        return self._motors_ft

    @property
    def is_connected(self) -> bool:
        return self.bus.is_connected and all(cam.is_connected for cam in self.cameras.values())

    @property
    def is_calibrated(self) -> bool:
        return set(self.calibration.keys()) == set(self.ALL_JOINTS)

    def connect(self, calibrate: bool = True) -> None:
        self.bus.connect()
        if not self.is_calibrated and calibrate:
            self.calibrate()

        for cam in self.cameras.values():
            cam.connect()

        self.configure()

    def calibrate(self) -> None:
        self.bus.disable_torque()
        for joint_name in self.ARM_JOINTS:
            self.bus.write("Operating_Mode", joint_name, OperatingMode.POSITION.value)
        self.bus.write("Operating_Mode", "gripper", OperatingMode.CURRENT_POSITION.value)

        input(
            "Move the OpenManipulator-X to a neutral pose (arm centered, gripper half open) "
            "and press ENTER to continue..."
        )
        homing_offsets = self.bus.set_half_turn_homings()

        print(
            "Move each joint slowly through its full safe range. "
            "Press ENTER when you are done recording the motion range."
        )
        range_mins, range_maxes = self.bus.record_ranges_of_motion()

        self.calibration.clear()
        for motor_name, motor in self.bus.motors.items():
            self.calibration[motor_name] = MotorCalibration(
                id=motor.id,
                drive_mode=self.config.drive_mode.get(motor_name, 0),
                homing_offset=homing_offsets[motor_name],
                range_min=range_mins[motor_name],
                range_max=range_maxes[motor_name],
            )

        self.bus.write_calibration(self.calibration)
        self._save_calibration()
        print(f"Calibration saved to {self.calibration_fpath}")

    def configure(self) -> None:
        with self.bus.torque_disabled():
            self.bus.configure_motors()
            for joint_name in self.ARM_JOINTS:
                self.bus.write("Operating_Mode", joint_name, OperatingMode.POSITION.value)
            self.bus.write("Operating_Mode", "gripper", OperatingMode.CURRENT_POSITION.value)
        self.bus.enable_torque()

    def get_observation(self) -> dict[str, Any]:
        if not self.is_connected:
            raise ConnectionError(f"{self} is not connected.")

        obs = self.bus.sync_read("Present_Position")
        obs_dict = {f"{motor_name}.pos": float(value) for motor_name, value in obs.items()}

        for cam_name, cam in self.cameras.items():
            obs_dict[cam_name] = cam.async_read()

        return obs_dict

    def send_action(self, action: dict[str, Any]) -> dict[str, Any]:
        if not self.is_connected:
            raise ConnectionError(f"{self} is not connected.")

        goal_pos = {key.removesuffix(".pos"): float(value) for key, value in action.items()}
        self.bus.sync_write("Goal_Position", goal_pos)
        return action

    def disconnect(self) -> None:
        for cam in self.cameras.values():
            cam.disconnect()
        self.bus.disconnect(disable_torque=self.config.disable_torque_on_disconnect)
