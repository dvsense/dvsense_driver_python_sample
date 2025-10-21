import time
from dvsense_driver.camera_manager import DvsCameraManager
from dvsense_driver.hal.dvs_camera_utils import CameraDescription

# 初始化相机管理器
dvs_camera_manager = DvsCameraManager()
dvs_camera_manager.update_cameras()

# 获取相机描述信息
camera_descriptions = dvs_camera_manager.get_camera_descs()
print("Available camera descriptions:", camera_descriptions)

# 检查是否有可用相机
if not camera_descriptions:
    print("No camera found. Exiting...")
    exit(0)

# 打印所有相机描述信息
for camera_description in camera_descriptions:
    print("Camera description:", camera_description)

# 尝试打开第一个可用的相机
try:
    camera = dvs_camera_manager.open_camera(camera_descriptions[0].serial)
except Exception as e:
    print(f"Failed to open camera: {e}")
    exit(1)

# 打印相机信息
print("Opened camera:", camera)

# 获取相机的宽度和高度
try:
    width = camera.get_width()
    height = camera.get_height()
    print(f"Camera resolution - Width: {width}, Height: {height}")
except Exception as e:
    print(f"Failed to retrieve camera resolution: {e}")
    camera.stop()
    exit(1)

# 启动相机并开始录制
try:
    camera.start()
    print("Camera started.")
    camera.start_recording("dvs-recording-file.raw")
    print("Recording started. Saving to 'dvs-recording-file.raw'...")
    time.sleep(5)  # 录制 5 秒
    camera.stop_recording()
    print("Recording stopped.")
except Exception as e:
    print(f"An error occurred during recording: {e}")
finally:
    # 停止相机
    camera.stop()
