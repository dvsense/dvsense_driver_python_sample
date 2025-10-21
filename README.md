# dvsense_driver_python_sample
针对dvsense_driver python库提供的python代码示例仓库

# 安装 dvsense_driver
在终端使用一下命令安装dvsense_driver
支持python版本: python3.8 - python3.12

~~~bash
pip install dvsense_driver
~~~

# 示例代码介绍

## dvslume_real_time_viewer.py
DvsLume相机实时预览示例，支持相机: DvsLume, EVK4

## camera_recording_sample.py
DvsLume相机raw文件录制示例

## dvslume_viewer_batch_events_by_time.py
DvsLume相机通过获取一定时间段内事件数据进行批量预览

## dvslume_viewer_batch_events.py
DvsLume相机通过获取一定数量的事件数据进行批量预览

## dvsync_camera_sample.py
DVSync相机实时预览示例，支持相机: DVSync

## dvsync_file_reader.py
DVSync 融合文件读取示例

## config_camera_params.py
相机参数的获取与配置

## raw_file_reader.py
raw事件数据文件读取示例

## raw_file_recorder_video_export_sample.py
raw事件数据文件导出视频示例

## 持续更新中...

# 注意事项
在对事件相机的数据进行实时处理过程中，由于python的运行效率问题，尽量避免for循环的使用