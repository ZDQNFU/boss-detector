import time
from detector import FaceDetector
from switcher import emergency_switch

# ==================== 配置参数 ====================
TRIGGER_FACE_COUNT = 2  # 检测到多少人脸时触发
COOLDOWN_SECONDS = 5  # 触发后的冷却时间（秒）
CHECK_INTERVAL = 0.2  # 检测间隔（秒），0.2 即每秒检测 5 次


# =================================================

def main():
    print("=" * 40)
    print("👀 Boss Detector 启动中...")
    print("=" * 40)

    # 初始化检测器
    try:
        detector = FaceDetector(
            known_faces_dir="known_faces",
            trigger_count=TRIGGER_FACE_COUNT
        )
    except Exception as e:
        print(f"初始化失败: {e}")
        print("请确保：")
        print("1. 摄像头可用")
        print("2. 已安装所有依赖（pip install -r requirements.txt）")
        print("3. 已下载 YOLO 人脸模型（首次运行会自动下载）")
        return

    last_trigger_time = 0
    is_triggered = False

    print("\n✅ 监控已开启，按下 Ctrl+C 退出\n")

    try:
        while True:
            # 检测当前画面
            should_trigger, face_count = detector.get_frame_and_detect()
            current_time = time.time()

            # 冷却检查
            if should_trigger and not is_triggered:
                if current_time - last_trigger_time > COOLDOWN_SECONDS:
                    print(f"[Main] 🚨 触发应急切换！")
                    emergency_switch()
                    last_trigger_time = current_time
                    is_triggered = True
                else:
                    # 还在冷却中，不重复触发
                    pass

            # 当人脸数恢复正常（≤1 且是已知人脸），重置触发状态
            if face_count <= 1 and not should_trigger:
                if is_triggered:
                    print("[Main] 环境安全，监控恢复")
                is_triggered = False

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\n[Main] 收到退出信号，正在关闭...")
    finally:
        detector.release()
        print("[Main] 摄像头已释放，程序结束。")


if __name__ == "__main__":
    main()
