These are LeRobot plugin skeletons for a custom OpenManipulator-X follower robot and leader teleoperator.

Current package layout:
- `lerobot_robot_openmanipulator_x`: follower robot plugin
- `lerobot_teleoperator_openmanipulator_x`: leader teleoperator plugin

Default follower camera setup:
- `front`: OpenCV camera at index `0`
- `around`: OpenCV camera at index `1`

-------------------------------------------------------------------------------------------------------------
 Robotics의 Openmanipulator 로봇과 ACT 모델의 Input 사양을 맞추기 위한 Plugin입니다.

Lerobot 가상 환경에서 아래에 명령어로 설치 한 후에 바로 진항하면 됩니다.

cd ~/lerobot_plugins/lerobot_robot_openmanipulator_x
pip install -e .

cd ~/lerobot_plugins/lerobot_teleoperator_openmanipulator_x
pip install -e .
