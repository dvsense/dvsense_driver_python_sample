from dvsense_driver import (
    Calibrator,
    CalibratorParameters,
    ApsFrame,
    DvsFileInfo,
)
from dvsense_driver.raw_file_reader import RawFileReader    
from dvsense_driver.mp4_file_reader import Mp4FileReader
import dvsense_driver
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

def fusion_events_to_image(aps_frame: ApsFrame, events):
    H = aps_frame.height()
    W = aps_frame.width()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    histgram = torch.zeros((2, H, W), dtype=torch.long, device=device)
    x = torch.tensor(events["x"].astype(np.int32), dtype=torch.long).to(device)
    x = -x
    y = torch.tensor(events["y"].astype(np.int32), dtype=torch.long).to(device)
    p = torch.tensor(events["polarity"].astype(np.int32), dtype=torch.long).to(device)

    torch.index_put_(histgram, (p, y, x), torch.ones_like(x), accumulate=True)

    on_hist, off_hist = histgram.cpu().numpy()

    aps_frame.data_numpy()[on_hist > 0] = COLOR_CODING["blue_red"]["on"]
    aps_frame.data_numpy()[off_hist > 0] = COLOR_CODING["blue_red"]["off"]

cv2.namedWindow("fusion", cv2.WINDOW_NORMAL)

dvs_file_path = "C:/DVSense/filedata/DVSyncRecTest/python_test_rec.raw"
aps_file_path = "C:/DVSense/filedata/DVSyncRecTest/python_test_rec.mp4"
json_file_path = "C:/DVSense/filedata/DVSyncRecTest/python_test_rec.json"

dvs_file_reader = RawFileReader(dvs_file_path)
aps_file_reader = Mp4FileReader(aps_file_path)
calibrator = Calibrator()
calib_param = CalibratorParameters()
dvsense_driver.json_file_to_param(json_file_path, calib_param)
calibrator.load_calibrator_param(calib_param)
dvs_file_reader.load_file()
aps_file_reader.load_file()

file_info = DvsFileInfo()
if dvs_file_reader.get_file_info(file_info):
    print("file info:", file_info)
mp4_time_offset = file_info.aps_start_timestamp
print("Mp4 time offset:", mp4_time_offset)
while True:
    aps_frame = ApsFrame()
    if(aps_file_reader.get_next_frame(aps_frame)):
        print("aps frame:", aps_frame.exposure_end_timestamp)
        aps_dvs_ts = aps_frame.exposure_end_timestamp + mp4_time_offset
        events = dvs_file_reader.get_n_time_events(aps_dvs_ts-33333, 33333)
        if(events.size > 0):
            print("events start time:", events[1]["timestamp"], " end time:", events[-1]["timestamp"])
            aps_frame_dvs_size = calibrator.map_aps_to_dvs(aps_frame)
            fusion_events_to_image(aps_frame_dvs_size, events)
            cv2.imshow("fusion", aps_frame_dvs_size.data_numpy())
            key = cv2.waitKey(1000)
    else:
        break


