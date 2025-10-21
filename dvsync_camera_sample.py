from dvsense_driver import (
    DvsCameraManager,
    DvsApsFusionProccessor,
    Calibrator,
    CalibratorParameters,
    ApsFrame,
)

import numpy as np
import torch
import cv2
import time
import threading
import numpy as np
import cv2
import threading

COLOR_CODING: dict = {
    "blue_red": {"on": [0, 0, 255], "off": [255, 0, 0], "bg": [0, 0, 0]},
    "blue_white": {"on": [216, 223, 236], "off": [201, 126, 64], "bg": [0, 0, 0]},
}
is_recording = False
is_playing = False
imwindow_name = "DVSync: APS + Events (Red:+, Blue:-)"
front_disp_buffer = None
back_disp_buffer = None
buffer_lock = threading.Lock()

dvs_camera_manager = DvsCameraManager()
dvs_camera_manager.update_cameras()
camera_descs = dvs_camera_manager.get_camera_descs()

dvs_aps_fusion_proccessor = DvsApsFusionProccessor()
calib = Calibrator()
open_camera_serial = camera_descs[0].serial
for camera_desc in camera_descs:
    print(camera_desc)
    if camera_desc.product == "DVSync":
        open_camera_serial = camera_desc.serial
        print("Open DVSync camera:", open_camera_serial)
        break
camera = dvs_camera_manager.open_fusion_camera(open_camera_serial)
print(camera)
param = CalibratorParameters()
camera.read_calibration_parameter(param)
print(param)
calib.load_calibrator_param(param)

def fusion_events_to_image(aps_frame: ApsFrame, events):
    H = aps_frame.height()
    W = aps_frame.width()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    histgram = torch.zeros((2, H, W), dtype=torch.long, device=device)
    x = torch.tensor(events["x"].astype(np.int32), dtype=torch.long).to(device)
    y = torch.tensor(events["y"].astype(np.int32), dtype=torch.long).to(device)
    p = torch.tensor(events["polarity"].astype(np.int32), dtype=torch.long).to(device)

    torch.index_put_(histgram, (p, y, x), torch.ones_like(x), accumulate=True)

    on_hist, off_hist = histgram.cpu().numpy()

    aps_frame.data_numpy()[on_hist > 0] = COLOR_CODING["blue_red"]["on"]
    aps_frame.data_numpy()[off_hist > 0] = COLOR_CODING["blue_red"]["off"]

def on_event_callback(events):
    dvs_aps_fusion_proccessor.add_dvs_data(events)


def on_frame_callback(frame):
    dvs_aps_fusion_proccessor.add_aps_data(frame)


def on_sync_signal_callback(trigger_in):
    dvs_aps_fusion_proccessor.add_sync_signal(trigger_in)


def on_fusion_data_callback(aps_frame, events):
    global front_disp_buffer, back_disp_buffer

    frame_dvs_size = calib.map_aps_to_dvs(aps_frame)
    fusion_events_to_image(frame_dvs_size, events)

    with buffer_lock:
        back_disp_buffer = frame_dvs_size.data_numpy()
        front_disp_buffer, back_disp_buffer = back_disp_buffer, front_disp_buffer

event_cb_id = camera.add_event_stream_nocopy_callback(on_event_callback)
aps_cb_id = camera.add_aps_frame_nocopy_callback(on_frame_callback)
sync_signal_cb_id = camera.add_sync_signal_callback(on_sync_signal_callback)
dvs_aps_fusion_proccessor.add_fusion_data_callback(on_fusion_data_callback)

# camera.write_calibration_file('./python_test_rec.json') // 如果重新标定，需要写入标定文件
print(type(camera))
camera.start()
is_playing = True
display_image = np.zeros((480, 640, 3), np.uint8)

while is_playing and camera.is_connected():
    with buffer_lock:
        if front_disp_buffer is not None:
            display_image = front_disp_buffer.copy() 
        else:
            display_image = np.zeros((480, 640, 3), np.uint8)

    cv2.imshow(imwindow_name, display_image)
    key = cv2.waitKey(33) & 0xFF
    if key == ord("q"):
        camera.stop()
        print("Exit")
        cv2.destroyAllWindows()
        break
    elif key == ord(" "):
        if is_recording:
            camera.stop_recording()
            is_recording = False
        else:
            camera.start_recording("C:/DVSense/filedata", "python_test_rec")
            is_recording = True
