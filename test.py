from datetime import datetime, timedelta
import random

def generate_datetime(start_date: datetime, end_date: datetime, nb_logs:int) -> list[datetime]:
    """
    Generate a random datetime between start_date and end_date.
    """
    timestamps = []
    total_seconds = (end_date - start_date).total_seconds()
    for _ in range(nb_logs):
        random_offset = random.random()*total_seconds
        timestamp = start_date + timedelta(seconds=random_offset)
        timestamps.append(timestamp)
    timestamps.sort()
    return timestamps

start = datetime(2025, 1, 1)
end = datetime(2026, 1, 2)
logs = generate_datetime(start, end, 5)
print(logs)

seconde = end - start


random_second = random.random()*seconde.total_seconds()
print(random_second)
timestamp = start + timedelta(seconds =random_second)
print(timestamp)

