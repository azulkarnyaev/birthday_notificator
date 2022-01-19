from datetime import datetime


def extract_date_key(event) -> str:
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    event_time = datetime.strptime(event['time'], date_format).date()
    return f"{event_time.day}#{event_time.month}"

