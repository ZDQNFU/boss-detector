# 👀 Boss Detector (反监控版摸鱼Agent)

一个基于 YOLO 人脸检测的智能“老板键”工具。它利用笔记本摄像头实时监测，一旦发现“非本人”或“多张脸”进入视野，瞬间切换到预设的工作界面。**不是帮你工作，是帮你更安全地不工作。**

> ⚠️ **免责声明**：本项目仅供计算机视觉技术学习与交流，请勿在严肃工作场合实际使用。摸鱼有风险，被抓后果自负。😏

## ✨ 核心特性

- **🚀 极速响应**：基于 YOLOv8 轻量级模型，CPU 也能跑 30fps，延迟低于 0.1 秒，比老板的脚步更快。
- **🧠 智能判断**：区分“自己”和“他人”，只有检测到 **多人** 或 **陌生人脸** 才触发切换。
- **🖥️ 隐蔽切换**：自动切到 Windows 虚拟桌面或预设工作软件，同时支持自动静音。
- **🔒 隐私保护**：**100% 本地运行**，图像数据不上传云端，无需联网。

## 🛠️ 技术栈

| 组件 | 作用 | 备注 |
| :--- | :--- | :--- |
| **YOLOv8** | 实时人脸检测 | 使用 `ultralytics` 预训练模型 |
| **face_recognition** | 人脸特征比对 | 基于 dlib，精准识别“自己” |
| **PyAutoGUI** | 模拟键盘快捷键 | 执行切换桌面、静音等操作 |
| **OpenCV** | 摄像头画面捕获 | 高效处理视频流 |

## 📁 项目结构

```text
brower_agent/
├── main.py                # 主程序入口
├── detector.py            # 人脸检测与识别逻辑
├── switcher.py            # 应急切换动作模块
├── requirements.txt       # Python 依赖包列表
├── known_faces/           # 存放“自己”的照片用于注册
│   └── me.jpg
└── README.md              # 说明文件

⚠️ 可能遇到的问题
1. ImportError: cannot import name '_pyautogui_win' from partially initialized module 'pyautogui'

```python
pip uninstall pyautogui -y
pip install --no-cache-dir --force-reinstall pyautogui==0.9.54

2.  face_recognition_models相关问题

```python
pip uninstall face-recognition-models -y
pip install --no-cache-dir git+https://github.com/ageitgey/face_recognition_models

