# dvsense_driver_python_sample

[中文](README.md)

This repository provides sample code based on the `dvsense_driver` Python library, helping users quickly get started with the development and application of [dvsense](https://www.dvsense.com/) event cameras.

## Installation

Supported Python versions: **3.8 – 3.12**

Run the following command in your terminal to install `dvsense_driver`:

```bash
pip install dvsense_driver
```

## Sample Code Overview

- **dvslume_real_time_viewer.py**  
    Real-time preview sample for [DVSLume](https://www.dvsense.com/products/dvslume/) cameras. Supports DvsLume and EVK4 cameras.

- **camera_recording_sample.py**  
    Raw file recording sample for [DVSLume](https://www.dvsense.com/products/dvslume/) cameras.

- **dvslume_viewer_by_time.py**  
    Batch retrieval and preview of [DVSLume](https://www.dvsense.com/products/dvslume/) camera event data by time interval.

- **dvslume_viewer_by_events.py**  
    Batch retrieval and preview of [DVSLume](https://www.dvsense.com/products/dvslume/) camera event data by event count.

- **dvsync_viewer.py**  
    Real-time preview sample for [DVSync](https://www.dvsense.com/products/dvsync/) cameras.

- **dvsync_file_reader.py**  
    Fused file reading sample for [DVSync](https://www.dvsense.com/products/dvsync/).

- **config_camera_params.py**  
    Sample for retrieving and configuring camera parameters. For detailed parameter configuration, refer to the [official documentation](https://sdk.dvsense.com/zh/html/tools_zh.html).

- **raw_file_reader.py**  
    Raw event data file reading sample.

- **raw_file_recorder_video_export_sample.py**  
    Sample for exporting raw event data files to video.

More samples are continuously being added — stay tuned!

## Notes

- When processing event camera data in real time, avoid using `for` loops in Python code whenever possible to improve runtime efficiency.
