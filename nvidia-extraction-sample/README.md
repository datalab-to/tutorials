# NVIDIA Q2 FY27 extraction sample

A small benchmark: one NVIDIA earnings release, two schemas that ask for the
same four numbers, and a gold answer for each. The two schemas differ in one
field. `precise` asks for `quarter_non_gaap_diluted_eps_usd`, and `vague` asks
for `diluted_eps_usd`, which could mean either GAAP or non-GAAP.

Install with:

```
uv sync
```

Here are the steps that we will run through:

1. Understanding our data.
2. Convert the data files into `omni_extract_bench` (`oeb`) format by running `create_manifest.py`. 
3. Run the benchmark.
4. Understand the results.

## 1. Understanding our data

A schema is a JSON Schema. The description on each field is what the
extractor is told:

```json
{
  "type": "object",
  "properties": {
    "quarter_end": {"type": "string", "format": "date", "description": "..."},
    "quarter_revenue_usd_millions": {"type": "number", "description": "..."},
    "quarter_gaap_diluted_eps_usd": {"type": "number", "description": "..."},
    "quarter_non_gaap_diluted_eps_usd": {"type": "number", "description": "..."}
  },
  "required": ["quarter_end", "..."],
  "additionalProperties": false
}
```

A gold file is the answer the schema should produce:

```json
{
  "quarter_end": "2026-07-26",
  "quarter_revenue_usd_millions": 96221,
  "quarter_gaap_diluted_eps_usd": 2.46,
  "quarter_non_gaap_diluted_eps_usd": 2.22
}
```

In this example we use the same input document but with two different schemas: one is *precise* and one is *vague*. Specifically, we're looking for non-GAAP diluted earnings per share for the most recent quarter. The precise key and description is:

```json
"quarter_non_gaap_diluted_eps_usd": {
    "type": "number",
    "description": "Current quarter non-GAAP diluted earnings per share in USD per share as presented in this release."
  }
```

while the vague key and description is:

```json
"diluted_eps_usd": {
    "type": "number",
    "description": "Diluted earnings per share for Q2 FY27 from the financial summary tables, in USD per share."
  }
```

We will see how this schema design affects performance. 

## 2. Creating the manifest

`oeb` expects datasets in a pretty flexible format. However as it currently stands we do not have it. It revolves around a `manifest.parquet` where each row describes one dataset element.

For `oeb`, there are certain columns that are required:

- `doc_id (str)`: an id for the dataset element; it must be unique, ignoring case.
- `doc_path (path)`: a relative path to the document. 
- `gt_path (path)`: a relative path to the ground truth json whose filename is the value for `id`.
- `schema (bytes)`: the extraction schema stored inline in the parquet.
- `suite (str | None)`: where the document came from; a null suite is read as `"other"`.

The thing to note is that both paths are relative to the dataset folder and stay inside it. `gt_path` can live in any subfolder, but its filename must be `<doc_id>.json`. `doc_path` can have any name, and several rows can share one document: here both schemas read the same PDF. For example:

```json
{"doc_id": "nvidia_q2_fy27_precise", "doc_path": "docs/nvidia_q2_fy27.pdf", "gt_path": "gold/nvidia_q2_fy27_precise.json", "schema": ..., "suite": "nvidia"}
```

We will run `create_manifest.py` which generates the `manifest.parquet` in `data` from our files:

```
uv run python create_manifest.py
```

We can check that `oeb` can run the dataset. This is helpful if you're bringing your own dataset:

```
uv run oeb check --dataset data
```

## 3. Run the benchmark

We provide two ways of running the benchmark. Because our dataset now follows the `oeb` layout, we can immediately run a benchmark on any of the registered providers on it. For example, 

```
uv run oeb benchmark --providers datalab --dataset data
```

This handles the orchestration of prediction, scoring, and writing to disk the results Alternatively, we supply a minimal loop in `run.py` which is more specific to this example and doesn't save results but shows you how you can create your own benchmark "loop" with the `predict` and `score` primitives. You can run that with 

```
uv run python run.py
```

## 4. Understand the results

If you ran with `oeb benchmark ...` you will find a `runs/` folder from where you ran the command. This contains the following

```
runs/
  datalab-<hash>
      predictions/<id>.json
      records/<id>.json
      verdicts/
      scores.jsonl
      settings.json
      summary.json
```

Let's go through the files in the order they're written:

- `settings.json` writes at the beginning which tells us what settings we passed and on what dataset. We didn't pass any settings for `datalab` so we use its default. 
- `records/` and `predictions/` are folders with `json` files, one for each row in the manifest and linked via `<id>` filename.
  - A file in `predictions/` is the answer. Scoring only in our benchmark loop only uses this file. It also allows you to bring your own predictions and run `oeb grade`. 
  - A file in `records/` contains the answer as well as the raw response from the API. This helps with observability.
- `verdicts/` contain more detailed information about the scoring for extraction. See our [blog post](https://www.datalab.to/blog/omni-extract-bench) or [github](https://github.com/datalab-to/omni_extract_bench/tree/main) for more information on those.
- `scores.jsonl` provides the scores for each row. 
- `summary.json` provides an aggregation of the per-row scores. 

Let's actually look at what happened here. If we look through the `scores.jsonl` we get one row perfectly and one row with a `misread`:

```jsonl
{"doc_id": "nvidia_q2_fy27_precise", ..., "accuracy": 1.0, "precision": 1.0, "recall": 1.0, ..., "matched": 4, "misread": 0, ...}
{"doc_id": "nvidia_q2_fy27_vague", ..., "accuracy": 0.75, "precision": 0.75, "recall": 0.75, ..., "matched": 3, "misread": 1, ...}
```

We can see the exact misread in `verdicts/nvidia_q2_fy27_vague.jsonl`. For visualization we'll run a small script to print it out nicely:

```
uv run python pretty_print_verdicts.py
```

```
--- k.diluted_eps_usd
pred:   2.46
gt:     2.22
result: misread
--- k.quarter_end
pred:   #d2026-07-26
gt:     #d2026-07-26
result: matched
--- k.quarter_gaap_diluted_eps_usd
pred:   2.46
gt:     2.46
result: matched
--- k.quarter_revenue_usd_millions
pred:   96221
gt:     96221
result: matched
```

We see that the `diluted_eps_usd` key was misread. This is a function of the schema being *vague* for what we actually wanted. 