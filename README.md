These are LeRobot plugin skeletons for a custom OpenManipulator-X follower robot and leader teleoperator.

Current package layout:
- `lerobot_robot_openmanipulator_x`: follower robot plugin
- `lerobot_teleoperator_openmanipulator_x`: leader teleoperator plugin

Default follower camera setup:
- `front`: OpenCV camera at index `0`
- `around`: OpenCV camera at index `1`

If your USB camera order is different, update the default camera indexes in
`lerobot_robot_openmanipulator_x/lerobot_robot_openmanipulator_x/config_openmanipulator_x_follower.py`.
