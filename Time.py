from datetime import datetime
import data

time_ranges = []

def getTime():
    data = data.fetch_data_from_api()
    print(data)

    time1_start = datetime.strptime("08:17", "%H:%M")
    time1_end = datetime.strptime("08:17", "%H:%M")
    time2_start = datetime.strptime("08:17", "%H:%M")
    time2_end = datetime.strptime("08:17", "%H:%M")
    time3_start = datetime.strptime("08:17", "%H:%M")
    time3_end = datetime.strptime("08:17", "%H:%M")

    time_ranges.append((
        time1_start, time1_end,
        time2_start, time2_end,
        time3_start, time3_end,
    ))

    processed_status = {
        (time_range, id): False for time_range in time_ranges for id in range(1, 5)
    }

def runTime():
    while True:
        current_time = datetime.now().strftime("%H:%M")  # เวลาปัจจุบันในรูปแบบ HH:MM
        received_time = datetime.strptime(current_time, "%H:%M")  # แปลงสตริงเวลาเป็น datetime object
        has_processed = False

        print(current_time)

        id_input = int(input("Enter ID (1-4): "))

        for index, (start_time, end_time) in enumerate(time_ranges):
            if start_time <= received_time <= end_time:
                if not processed_status[((start_time, end_time), id_input)]:
                    processed_status[((start_time, end_time), id_input)] = True
                    print(f"process ID {id_input}")
                    has_processed = True
                else:
                    print(f"ID {id_input} Already processed")
                    has_processed = True
                break

        if not has_processed:
            print("NO process")

        if datetime.now().hour == 0 and datetime.now().minute == 0:
            processed_status = {(time_range, id): False for time_range in time_ranges for id in range(1, 5)}


