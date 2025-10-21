import numpy as np
import cv2
import torch
from dvsense_driver.camera_manager import DvsCameraManager
from dvsense_driver.hal.dvs_camera_utils import CameraDescription

# 初始化相机管理器
dvs_camera_manager = DvsCameraManager()
dvs_camera_manager.update_cameras()

# 获取相机描述信息
camera_descriptions = dvs_camera_manager.get_camera_descs()
print(camera_descriptions)

# 检查是否有可用相机
if not camera_descriptions:
    print("No camera found. Exiting...")
    exit(0)

# 打印所有相机描述信息
for camera_desc in camera_descriptions:
    print(camera_desc)

# 打开第一个可用的相机
try:
    camera = dvs_camera_manager.open_camera(camera_descriptions[0].serial)
except Exception as e:
    print(f"Failed to open camera: {e}")
    exit(1)

# 打印相机信息
print(camera)

# 获取相机的宽度和高度
width = camera.get_width()
height = camera.get_height()

# 定义颜色编码字典
COLOR_CODING: dict = {
    'blue_red': {
        'on': [0, 0, 255],
        'off': [255, 0, 0],
        'bg': [0, 0, 0]
    },
    'blue_white': {
        'on': [216, 223, 236],
        'off': [201, 126, 64],
        'bg': [0, 0, 0]
    }
}

# 启动相机并设置累帧时长
camera.start()
camera.set_batch_events_time(10000)  # 设置累帧时长为 10 毫秒

# 实时显示事件流
while True:
    # 获取事件数据
    events = camera.get_next_batch()

    # 初始化数据
    histogram = torch.zeros((2, height, width), dtype=torch.long)

    # 提取事件的 x、y 坐标和极性
    x_coords: torch.Tensor = torch.tensor(events['x'].astype(np.int32), dtype=torch.long)
    y_coords: torch.Tensor = torch.tensor(events['y'].astype(np.int32), dtype=torch.long)
    polarities: torch.Tensor = torch.tensor(events['polarity'].astype(np.int32), dtype=torch.long)

    # 更新数据
    torch.index_put_(
        histogram, (polarities, y_coords, x_coords), torch.ones_like(x_coords), accumulate=False
    )
    _, hist_height, hist_width = histogram.shape

    # 定义颜色编码
    color_coding: dict = COLOR_CODING['blue_white']

    # 初始化画布
    canvas = np.zeros((hist_height, hist_width, 3), dtype=np.uint8)
    canvas[:, :] = color_coding['bg']

    # 将数据转换为 NumPy 数组
    off_histogram, on_histogram = histogram.cpu().numpy()

    # 根据事件极性更新画布颜色
    canvas[on_histogram > 0] = color_coding['on']
    canvas[off_histogram > 0] = color_coding['off']

    # 显示事件图像
    cv2.imshow('events', canvas)

    # 按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cv2.destroyAllWindows()
camera.stop()