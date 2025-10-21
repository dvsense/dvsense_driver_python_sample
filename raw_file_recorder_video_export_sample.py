from dvsense_driver.camera_manager import DvsCameraManager
from dvsense_driver.hal.dvs_camera_utils import CameraDescription
from dvsense_driver.raw_file_reader import RawFileReader

file_reader = RawFileReader('/mnt/d/ubuntu/20250421_154907.raw')
if file_reader.load_file():
    _, t1 = file_reader.get_start_timestamp()
    _, t2 = file_reader.get_end_timestamp() 
    print("File loaded successfully.")
    if file_reader.export_event_to_video(t1, t2, "/mnt/d/ubuntu/test.mp4"):
        print("Video exported successfully.")
else:
    print("File loaded failed.")
