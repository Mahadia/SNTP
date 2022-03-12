import os, json
from datetime import datetime

log_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
results = { "timestamp": log_time,
            "winner": "Init",
            "new": {"loss": 0.29, "accuracy": 0.89},
            "old": {"loss": None, "accuracy": None}}
with open("logging.json", 'w+') as fl:
    init_log = {"logs": [results]}
    json.dump(init_log, fl)
