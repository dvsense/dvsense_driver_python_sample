import time
from dvsense_driver.raw_file_reader import RawFileReader    

if __name__ == "__main__":
    file_path = "workspace/Data/scatter3.raw"
    file_reader = RawFileReader(file_path)
    file_reader.load_file()
    acc_time = 10000 # in ms

    try:
        width = file_reader.get_width()
        height = file_reader.get_height()
        print(f"Camera resolution - Width: {width}, Height: {height}")
        time.sleep(2)

        start_timestamp = file_reader.get_start_timestamp()
        end_timestamp = file_reader.get_end_timestamp()
        print(f"Start timestamp: {start_timestamp}, End timestamp: {end_timestamp}")
        while True:
            events = file_reader.get_n_time_events(acc_time)
            current_pos_timestamp = file_reader.get_current_pos_timestamp()
            current_pos_event_num = file_reader.get_current_pos_event_num()
            print(f"current_pos_timestamp: {current_pos_timestamp}, current_pos_event_num: {current_pos_event_num}")
            print(f"events num: {events.shape[0]}")
            if current_pos_timestamp +acc_time>= end_timestamp[1]:
                break

    except KeyboardInterrupt:
        print("Stopping file reader...")
    finally:
        # file_reader.close()
        print("file reader closed.")    

