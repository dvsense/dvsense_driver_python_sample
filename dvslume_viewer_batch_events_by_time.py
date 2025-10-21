import numpy as np
import cv2
from dvsense_driver.camera_manager import DvsCameraManager
from dvsense_driver.hal.dvs_camera_utils import CameraDescription

# 初始化相机管理器
dvs_camera_manager = DvsCameraManager()
dvs_camera_manager.update_cameras()
camera_descriptions = dvs_camera_manager.get_camera_descs()

# 打印可用的相机信息
if not camera_descriptions:
    print("No camera found. Exiting...")
    exit(0)

for camera_desc in camera_descriptions:
    print(camera_desc)

try:
    # 打开第一个可用的相机
    camera = dvs_camera_manager.open_camera(camera_descriptions[0].serial)
except Exception as e:
    print(f"Failed to open camera: {e}")
    exit(1)

print(camera)

# 获取相机的宽度和高度
width = camera.get_width()
height = camera.get_height()

# 启动相机并设置累帧时长
camera.start()
camera.set_batch_events_time(10000)  # 设置获取事件时间为 10 毫秒

# 获取数据
events = camera.get_next_batch()

# 初始化画布
canvas = np.zeros((height, width, 1), dtype=np.uint8)

# 遍历事件数据并更新画布
for event in events:
    x = event['x']
    y = event['y']
    polarity = event['polarity']

    if polarity:
        canvas[y, x] = 255

camera.stop()

# 显示事件流
cv2.imshow('Event Stream', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
