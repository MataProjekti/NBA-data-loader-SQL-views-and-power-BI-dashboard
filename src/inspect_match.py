import json
from pathlib import Path

files = sorted(Path("data").glob("matches_*.json"))
data = json.loads(files[-1].read_text(encoding="utf-8"))


def flatten(obj, prefix=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from flatten(v, f"{prefix}.{k}" if prefix else k)
    elif isinstance(obj, list):
        yield prefix, f"lista od {len(obj)}"
        if obj:
            yield from flatten(obj[0], prefix + "[0]")
    else:
        yield prefix, repr(obj)


print("Fajl:", files[-1].name)
for path, value in flatten(data["matches"][0]):
    print(f"{path:45} {value[:70]}")