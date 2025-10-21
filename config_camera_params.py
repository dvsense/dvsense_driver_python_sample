from dvsense_driver.camera_manager import DvsCameraManager
from dvsense_driver.hal.dvs_camera_utils import CameraDescription
from dvsense_driver.hal.camera_tool import ToolType, CameraTool
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
for camera_description in camera_descriptions:
    print(camera_description)

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
print(f"Camera resolution - Width: {width}, Height: {height}")

# 遍历所有工具类信息
# all_tool_info = camera.get_all_tools_info()
# for tool_info in all_tool_info:
#     # print(tool_info)
#     tool = camera.get_tool(tool_info.tool_type)
#     for name, basic_param_info in tool.get_all_param_info().items():
#         print(basic_param_info)
#         print(tool.get_param_info(name)[1])
#         ret, param_info = tool.get_param_info(name)
#         ret, current_value = tool.get_param(name)
#         print(f"Current value: {current_value}, Default value: {param_info.default_value}")

# 单独获取特定工具类信息
bias_tool = camera.get_tool(ToolType.BIAS)
bias_tool.set_param('bias_diff_on', 0)

# trigger_in_tool = camera.get_tool(ToolType.TOOL_TRIGGER_IN)
# trigger_in_tool.set_param('enable', True)
