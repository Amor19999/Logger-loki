import requests
import json
import datetime

# --- Конфігурація ---
LOKI_URL = "http://10.129.0.11:3100"  # Адреса твого Loki

# LogQL-запит (заміни на свій, якщо потрібно)
LOGQL_QUERY = '{service="analytics-api", service_name="analytics-api"}'

# --- Діапазон часу ---
# Початок: 2025-06-30 23:00:00 UTC
start_dt = datetime.datetime(2025, 6, 30, 23, 0, 0, tzinfo=datetime.timezone.utc)
start_time_ns = int(start_dt.timestamp() * 1e9)

# Кінець: 2025-07-03 22:20:00 UTC
end_dt = datetime.datetime(2025, 7, 3, 22, 20, 0, tzinfo=datetime.timezone.utc)
end_time_ns = int(end_dt.timestamp() * 1e9)

LIMIT = 1000
DIRECTION = "backward"

def query_loki(query, start_ns, end_ns, limit=1000, direction="backward"):
    endpoint = f"{LOKI_URL}/loki/api/v1/query_range"
    params = {
        "query": query,
        "start": start_ns,
        "end": end_ns,
        "limit": limit,
        "direction": direction
    }
    print(f"Querying Loki endpoint: {endpoint}")
    print(f"With parameters: {params}")
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        return None

if __name__ == "__main__":
    print("Attempting to retrieve logs from Loki...")
    loki_response = query_loki(LOGQL_QUERY, start_time_ns, end_time_ns, LIMIT, DIRECTION)
    if loki_response and loki_response.get("status") == "success":
        data = loki_response.get("data")
        if data and data.get("resultType") == "streams":
            streams = data.get("result", [])
            if streams:
                print(f"\nSuccessfully retrieved {len(streams)} log streams.")
                total_log_entries = 0
                for stream in streams:
                    stream_labels = stream.get("stream", {})
                    log_values = stream.get("values", [])
                    total_log_entries += len(log_values)
                    print(f"\n--- Stream Labels: {stream_labels} ---")
                    for entry_ns, log_line in log_values:
                        # Перетворення наносекунд у datetime
                        timestamp_s = int(entry_ns) / 1e9
                        dt_object = datetime.datetime.fromtimestamp(timestamp_s, datetime.timezone.utc)
                        print(f"[{dt_object.isoformat()}] {log_line}")
                print(f"\nTotal log entries retrieved: {total_log_entries}")
            else:
                print("No log streams found for the given query and time range.")
        else:
            print("Loki response data format is not as expected.")
    else:
        print("Failed to get a response from Loki.")
