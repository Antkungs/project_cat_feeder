from datetime import datetime
import data

data = data.fetch_data_from_api()
time_ranges = []

for item in data:
    time1 = datetime.strptime(item["time1"], "%H:%M:%S")
    time2 = datetime.strptime(item["time2"], "%H:%M:%S")
    time3 = datetime.strptime(item["time3"], "%H:%M:%S")
    
    # Append the parsed times to the time_ranges list
    time_ranges.append((time1, time2, time3))

print(time_ranges)