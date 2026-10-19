"""Runs manifest.parquet through Datalab (balanced): predict, then score."""

import json
import pathlib
import pyarrow
import pyarrow.parquet

import omni_extract_bench as oeb
from omni_extract_bench import harness

ROOT = pathlib.Path(__file__).parent / "data"


def run(task: dict) -> dict:
  """The score of Datalab on `task`, or its error."""
  schema = json.loads(task["schema"])
  record = harness.predict(
    "datalab", ROOT / task["doc_path"], schema, mode="balanced"
  )
  if record["error"]:
    return {"error": record["error"]["message"]}
  gold = json.loads((ROOT / task["gt_path"]).read_text())
  return oeb.score(record["result"], gold, schema)


if __name__ == "__main__":
  for task in pyarrow.parquet.read_table(ROOT / "manifest.parquet").to_pylist():
    out = run(task)
    print(
      task["doc_id"], out.get("accuracy"), out.get("f1"), out.get("error", "")
    )
