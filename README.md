<p align="center">
  <img src="assets/datalab-logo.png" alt="Datalab Logo" width="150"/>
</p>
<h1 align="center">Datalab</h1>
<p align="center">
  <strong>State of the Art models for Document Intelligence</strong>
</p>
<p align="center">
  <a href="https://discord.gg/KuZwXNGnfH"><img src="https://img.shields.io/badge/Discord-Join%20us-5865F2?logo=discord&logoColor=white" alt="Discord"></a>
</p>
<p align="center">
  <a href="https://www.datalab.to"><img src="https://img.shields.io/badge/Homepage-datalab.to-blue" alt="Homepage"></a>
  <a href="https://documentation.datalab.to"><img src="https://img.shields.io/badge/Docs-Read%20the%20docs-blue" alt="Docs"></a>
  <a href="https://www.datalab.to/playground"><img src="https://img.shields.io/badge/Playground-Try%20it-orange" alt="Public Playground"></a>
</p>

<hr/>

# Tutorials

This repository has sample code from Datalab blog posts and guides. Each folder is one example and has its own README.

Datalab converts documents (PDFs, images, and office files) into Markdown, HTML, JSON, and structured data. The Datalab API does layout analysis, OCR (optical character recognition), table recognition, and schema-based extraction. Datalab also makes the open-source projects [marker](https://github.com/datalab-to/marker), [surya](https://github.com/datalab-to/surya), [chandra](https://github.com/datalab-to/chandra), [lift](https://github.com/datalab-to/lift), and [indra](https://github.com/datalab-to/indra).

## Get an API key

Most examples need a Datalab API key.

1. Go to [datalab.to](https://www.datalab.to/?utm_source=gh-tutorials) and sign up. You get $20 in free credits each month.
2. Make an API key on the [API keys page](https://www.datalab.to/app/keys).
3. Set the key in your shell:

   ```shell
   export DATALAB_API_KEY=...
   ```

To try Datalab without code, use the [public playground](https://www.datalab.to/playground?utm_source=gh-tutorials).

## Examples

| Folder | Description |
|---|---|
| [nvidia-extraction-sample](nvidia-extraction-sample) | A small extraction benchmark. It has one NVIDIA earnings release and two schemas that ask for the same four numbers. One schema asks for non-GAAP (generally accepted accounting principles) diluted EPS (earnings per share). The other asks for "diluted EPS", which can mean GAAP or non-GAAP. The example runs Datalab extraction on both schemas and scores each answer against a gold answer with [omni-extract-bench](https://github.com/datalab-to/omni_extract_bench). |
