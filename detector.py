import cv2
import face_recognition
import os
from ultralytics import YOLO


class FaceDetector:
    def __init__(self, known_faces_dir="known_faces", trigger_count=2):
        """
        初始化检测器
        :param known_faces_dir: 存放自己照片的文件夹
        :param trigger_count: 触发切换的人脸数量阈值（>=2 意味着有第二人出现）
        """
        self.trigger_count = trigger_count

        # 加载 YOLO 人脸检测模型（轻量，速度快）
        self.yolo_model = YOLO('yolov8n-face.pt')  # 首次运行会自动下载

        # 加载"自己"的人脸编码
        self.known_face_encodings = self._load_known_faces(known_faces_dir)
        print(f"[Detector] 已加载 {len(self.known_face_encodings)} 张已知人脸")

        # 摄像头
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("无法打开摄像头，请检查设备")

        # ========== 新增：状态记录变量 ==========
        self.is_triggered = False  # 当前是否处于"触发状态"（已切换到工作桌面）
        self.safe_frame_count = 0  # 连续安全的帧数（用于防抖）
        self.SAFE_FRAMES_THRESHOLD = 5  # 需要连续多少帧安全才认为真正安全了

    def _load_known_faces(self, folder_path):
        """从文件夹加载自己的照片并生成人脸编码"""
        encodings = []
        if not os.path.exists(folder_path):
            print(f"[Detector] 警告：'{folder_path}' 文件夹不存在，将不会进行身份识别")
            return encodings

        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(folder_path, filename)
                image = face_recognition.load_image_file(image_path)
                # 每张照片可能有多张人脸，这里只取第一张
                face_encs = face_recognition.face_encodings(image)
                if face_encs:
                    encodings.append(face_encs[0])
                    print(f"[Detector] 已注册人脸: {filename}")
        return encodings

    def is_face_known(self, face_image):
        """判断画面中的人脸是否是'自己'"""
        if not self.known_face_encodings:
            return False  # 没有注册人脸时，默认所有脸都是"未知"

        # 尝试对传入的图片进行编码
        rgb_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb_image)
        if not encodings:
            return False

        # 与已知人脸比对
        match = face_recognition.compare_faces(self.known_face_encodings, encodings[0], tolerance=0.5)
        return any(match)

    def get_frame_and_detect(self):
        """
        捕获一帧，返回 (是否需要触发切换, 检测到的人脸数)
        """
        ret, frame = self.cap.read()
        if not ret:
            return False, 0

        # 1. YOLO 快速检测所有人脸位置
        results = self.yolo_model(frame)
        boxes = results[0].boxes
        face_count = len(boxes) if boxes is not None else 0

        # 2. 判断当前画面是否"危险"（需要切换）
        is_danger = False

        if face_count >= self.trigger_count:
            # 人脸数达标，危险
            is_danger = True
            print(f"[Detector] 检测到 {face_count} 张人脸")
        elif face_count == 1 and self.known_face_encodings:
            # 只有一张脸，判断是不是自己
            if not self.is_face_known(frame):
                is_danger = True
                print("[Detector] 检测到单张未知人脸")
        elif face_count == 0:
            # 没人脸，安全
            is_danger = False
        elif face_count == 1 and self.known_face_encodings and self.is_face_known(frame):
            # 只有自己，安全
            is_danger = False

        # ========== 状态机逻辑 ==========
        should_trigger = False

        if is_danger:
            # 危险状态：重置安全帧计数
            self.safe_frame_count = 0

            if not self.is_triggered:
                # 之前是安全的，现在变危险了 → 触发切换！
                should_trigger = True
                self.is_triggered = True
                print("[Detector] ⚠️ 从安全进入危险状态，触发切换")
            else:
                # 已经处于触发状态，不再重复触发
                pass
        else:
            # 安全状态：累加计数
            if self.is_triggered:
                self.safe_frame_count += 1

                # 连续多帧安全，才认为真正安全了（防抖）
                if self.safe_frame_count >= self.SAFE_FRAMES_THRESHOLD:
                    self.is_triggered = False
                    self.safe_frame_count = 0
                    print("[Detector] ✅ 环境恢复安全，重置监控状态")
            else:
                # 本来就是安全的，什么都不用做
                pass

        return should_trigger, face_count

    def release(self):
        """释放摄像头资源"""
        self.cap.release()
        cv2.destroyAllWindows()