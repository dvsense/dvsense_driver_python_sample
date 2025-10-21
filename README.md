# dvsense_driver_python_sample

本仓库提供了基于 `dvsense_driver` Python 库的示例代码，帮助用户快速上手事件相机的开发与应用。

## 安装说明

支持 Python 版本：**3.8 - 3.12**

在终端执行以下命令安装 `dvsense_driver`：

```bash
pip install dvsense_driver
```

## 示例代码说明

- **dvslume_real_time_viewer.py**  
    [DVSLume](https://www.dvsense.com/products/dvslume/)相机实时预览示例，支持 DvsLume、EVK4 相机。

- **camera_recording_sample.py**  
    [DVSLume](https://www.dvsense.com/products/dvslume/)相机 raw 文件录制示例。

- **dvslume_viewer_by_time.py**  
    按时间段批量获取 [DVSLume](https://www.dvsense.com/products/dvslume/)相机事件数据并预览。

- **dvslume_viewer_by_events.py**  
    按事件数量批量获取 [DVSLume](https://www.dvsense.com/products/dvslume/)相机事件数据并预览。

- **dvsync_viewer.py**  
    [DVSync ](https://www.dvsense.com/products/dvsync/)相机实时预览示例，支持 [DVSync ](https://www.dvsense.com/products/dvsync/)相机。

- **dvsync_file_reader.py**  
    [DVSync ](https://www.dvsense.com/products/dvsync/)融合文件读取示例。

- **config_camera_params.py**  
    相机参数的获取与配置示例。参数配置详情参考[官方说明](https://sdk.dvsense.com/zh/html/tools_zh.html)

- **raw_file_reader.py**  
    raw 事件数据文件读取示例。

- **raw_file_recorder_video_export_sample.py**  
    raw 事件数据文件导出为视频的示例。

更多示例持续更新中，敬请关注！

## 注意事项

- 实时处理事件相机数据时，建议尽量避免在 Python 代码中使用 `for` 循环，以提升运行效率。
