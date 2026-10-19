# /// script
# dependencies = ["pyarrow"]
# ///
"""Writes manifest.parquet: one row per schemas/<doc>/<variant>.json.

docs/<doc>.pdf
schemas/<doc>/<variant>.json
gold/<doc>_<variant>.json      named for its row's doc_id, as oeb requires
"""

import json
import pathlib
import pyarrow
import pyarrow.parquet

ROOT = pathlib.Path(__file__).parent / "data"


def row(schema: pathlib.Path) -> dict[str, str]:
  """The manifest row for the task `schema`, with paths relative to `ROOT`."""
  doc, variant = schema.parent.name, schema.stem
  doc_id = f"{doc}_{variant}"
  pdf = f"docs/{doc}.pdf"
  gold = f"gold/{doc_id}.json"
  for p in (pdf, gold):
    if not (ROOT / p).exists():
      raise FileNotFoundError(
        f"{schema.relative_to(ROOT)} needs {p}, which is missing."
      )
  return {
    "doc_id": doc_id,
    "suite": "nvidia",
    "doc_path": pdf,
    "gt_path": gold,
    "schema": json.dumps(json.loads(schema.read_text())),
  }


def manifest(root: pathlib.Path) -> pyarrow.Table:
  return pyarrow.Table.from_pylist(
    [row(s) for s in sorted(root.glob("schemas/*/*.json"))]
  )


if __name__ == "__main__":
  pyarrow.parquet.write_table(manifest(ROOT), ROOT / "manifest.parquet")
