import json
from collections import defaultdict
from datetime import datetime

with open("loki_raw.json", "r", encoding="utf-8") as f:
    loki_data = json.load(f)
logs = []
for stream in loki_data.get("data", {}).get("result", []):
    for ts, raw_msg in stream.get("values", []):
        try:
            msg = json.loads(raw_msg)
        except Exception:
            msg = {"raw": raw_msg}
        msg["_timestamp"] = int(ts)
        logs.append(msg)

stats = defaultdict(int)
for log in logs:
    time_str = log.get("time")
    if not time_str:
        continue
    try:
        dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        day = dt.date().isoformat()
        stats[day] += 1
    except Exception:
        continue

with open("loki_stats.json", "w", encoding="utf-8") as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)

print("Готово! Результат у loki_stats.json")
