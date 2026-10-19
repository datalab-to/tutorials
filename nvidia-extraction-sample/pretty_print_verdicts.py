from pathlib import Path
import json

fp = Path("./runs/datalab-f46415c9/verdicts/nvidia_q2_fy27_vague.jsonl")

with fp.open("r") as f:
    for l in f:
        data = json.loads(l) if l.strip() else None
        if data is None: continue
        addr = ".".join(data["address"][0])
        pr = data["pred_canon"]
        gt = data["gold_canon"]
        res = data["result"]
        print(f"--- {addr}\npred:   {pr}\ngt:     {gt}\nresult: {res}")
