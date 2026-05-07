
다만 위처럼 README 안에 `markdown` 코드블록을 그대로 넣으면 중간의 `bash` 코드블록 때문에 GitHub에서 깨질 수 있어. 실제 README에 넣을 때는 아래 버전을 그대로 쓰는 게 더 안전해.

```markdown
# OpenManipulator-X LeRobot Plugin

These are LeRobot plugin skeletons for a custom OpenManipulator-X follower robot and leader teleoperator.

## Current Package Layout

- `lerobot_robot_openmanipulator_x`: follower robot plugin
- `lerobot_teleoperator_openmanipulator_x`: leader teleoperator plugin

## Default Follower Camera Setup

- `front`: OpenCV camera at index `0`
- `around`: OpenCV camera at index `1`

If your USB camera order is different, update the default camera indexes in:

`lerobot_robot_openmanipulator_x/lerobot_robot_openmanipulator_x/config_openmanipulator_x_follower.py`

---

## 설명

ROBOTIS OpenManipulator-X 로봇과 LeRobot ACT 모델의 input 사양을 맞추기 위한 plugin입니다.

이 plugin은 다음 두 가지 역할을 합니다.

- OpenManipulator-X follower robot plugin
- OpenManipulator-X leader teleoperator plugin

LeRobot 가상환경에서 아래 명령어를 복사하여 실행하면 설치할 수 있습니다.

## Installation

```bash
cd ~/lerobot_plugins/lerobot_robot_openmanipulator_x
pip install -e .

cd ~/lerobot_plugins/lerobot_teleoperator_openmanipulator_x
pip install -e .
