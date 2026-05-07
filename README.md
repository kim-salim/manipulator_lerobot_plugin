# OpenManipulator-X LeRobot Plugin

These are LeRobot plugin skeletons for a custom OpenManipulator-X follower robot and leader teleoperator.

## Current Package Layout

- `lerobot_robot_openmanipulator_x`: follower robot plugin
- `lerobot_teleoperator_openmanipulator_x`: leader teleoperator plugin

## Default Follower Camera Setup

- `front`: OpenCV camera at index `0`
- `around`: OpenCV camera at index `1`

---

## 설명

ROBOTIS OpenManipulator-X 로봇과 LeRobot ACT 모델의 input 사양을 맞추기 위한 plugin입니다.

이 plugin은 다음 두 가지 역할을 합니다.

- OpenManipulator-X follower robot plugin
- OpenManipulator-X leader teleoperator plugin

LeRobot 가상환경에서 아래 명령어를 복사하여 실행하면 설치할 수 있습니다.

```markdown
```bash
cd ~/lerobot_plugins/lerobot_robot_openmanipulator_x
pip install -e .

```markdown
cd ~/lerobot_plugins/lerobot_teleoperator_openmanipulator_x
pip install -e .
```
## Picture
<img width="1290" height="723" alt="KakaoTalk_20260507_224844178" src="https://github.com/user-attachments/assets/82d13907-6f94-4668-8c4a-a75d6c3c63f7" />

