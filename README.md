<div align="center">

# Kurious

**The search engine your unstructured world was missing.**

Ask any question. Across every format you've got — PDFs, videos, tables, scans, transcripts. Get a grounded answer with citations back to the source span. In one API call.

[Quickstart](#getting-started) · [Examples](examples/) · [Discord](https://discord.gg/aintropy-community) · [Discussions](https://github.com/Kurious-AI/getting-started/discussions)

</div>

---

## Tagline

The digital and physical AI knowledge engine. From `pip install` to your first answer in **60 seconds** — to your own indexed corpus in under an hour.

---

## Introduction

Most RAG stacks make you a plumber.

You're not building search. You're chunking PDFs, fighting embedders, gluing vector stores to SQL routers, and writing the fifteenth piece of OCR fallback logic. The interesting question — *what is my data actually telling me?* — never gets asked.

Kurious flips that.

**One call ingests.** `client.projects.ingest(project_id, path)` handles upload, parsing, chunking, embedding, indexing — and for video, automatic transcription + frame embeddings + captioning. No worker queue to operate.

**One call answers.** `client.search.intelligent(...)` auto-routes between RAG, NL2SQL, and knowledge-graph retrieval. You write the question. Kurious picks the right tool.

**Every answer is grounded.** File + character span for documents. File + timestamp for video. No hallucinated references, no opaque rerankers, no "trust me."

This repo is your fastest path in. Two ways:

| | Mode | Best for | Time to first query |
|---|---|---|---|
| **Explore** | Copy a trial API key. Hit our demo corpora. | "Show me what this thing does." | **~60 seconds** |
| **Builder** | Run `kurious init`. Ingest your own data. | "I want to ship something with this." | **~30 minutes** |

---

## Why Kurious

| Building it yourself | With Kurious |
|---|---|
| Pick a vector DB. Pick an embedder. Pick a chunker. Pick a reranker. Wire them. Maintain them. | One SDK. One import. Three lines to a working answer. |
| Hand-roll NL2SQL for structured data. Hand-roll KG for entity questions. Decide which to call. | `intelligent()` routes for you, automatically. |
| Bolt on OCR + Whisper + a frame extractor for multimodal corpora. Hope they don't drift. | PDF / DOCX / MP4 / MP3 / CSV / Parquet — all auto-detected, one pipeline, one call. |
| Spend two weeks on citation infrastructure to keep the lawyers happy. | Every answer ships with spans + timestamps. By default. |
| Operate it. Page on it. Scale it. | Hosted, multi-tenant, project-scoped. Your job is the use case. |

> *We replaced a six-person retrieval team with one Kurious project and a SDK call.* — what we want you to say after week one.

---

## What can you build using Kurious?

These are the patterns that show up across our earliest customers. Each is a real call — not a brochure example.

**Internal Q&A across thousands of docs.** Point Kurious at your handbook + runbooks + policy library. Wire `client.search.intelligent(...)` behind a Slack bot. Done in an afternoon.

**Meeting & call intelligence.** Drop in recorded Zoom calls. Ask *"What did the customer say about renewal in March?"* Get back the exact 30-second clip with the timestamp.

**Contract review at scale.** Ingest 10,000 vendor agreements. Filter by clause, by party, by signing date — all in natural language. No bespoke NER.

**Mixed-modality research agents.** Combine quarterly filings (CSV), analyst PDFs, and earnings-call recordings (MP4) in one project. Ask cross-modal questions and Kurious blends evidence across them.

**Cross-corpus comparison.** Same question, twenty municipalities. See where positions diverge. Take action on the deltas.

If you have unstructured content and a question worth asking, Kurious is the substrate.

---

## Prerequisites

- Python **3.10+**
- A terminal, `pip`, and a few minutes
- That's it. No Docker, no infra, no other API keys.

---

## Getting started

### Step 1 — Explore Mode (60 seconds, no signup)

Copy a trial key. Hit five pre-indexed demo corpora — Louisville city council, Seattle council, NJ Open Data, a legal video archive, and ChemRAG. Watch it work.

**1. Install the SDK**

```bash
pip install artifacts-keyring                              # one-time
pip install "aintropy>=0.5.5,<0.6" \
  --index-url "https://pkgs.dev.azure.com/AIntropy-DevOps/Kurious-SDK/_packaging/kurious-sdk-pypi/pypi/simple/"
```

> The SDK lives on a private Azure Artifacts feed during beta. `artifacts-keyring` handles auth in one shot. Hitting `401`? See [Troubleshooting](#troubleshooting--faq).

**2. Export the trial key**

```bash
export KURIOUS_API_KEY="trial_REPLACE_ME"   # placeholder — real key ships with Explore Mode
```

**3. Ask your first question**

```python
import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])

louisville = next(p for p in client.projects.list().projects if "louisville" in p.name.lower())
result = client.search.intelligent(
    project_id=louisville.id,
    query="What did the council decide about affordable housing?",
    mode="quick",
)

print(result.answer)
for s in result.sources[:3]:
    print(f"  {s.get('filename', '?')} (score={s.get('score', 0):.2f})")
```

You just queried hundreds of hours of council video and got a grounded answer back. That's the whole loop.

Now [open `examples/`](examples/) — ten more runnable scripts. Find a video moment by topic. Filter by date. Cross-modal queries. Compare two cities side by side. Each ~15 lines. Each runs on the same trial key.

### Step 2 — Builder Mode (your own data, ~30 minutes)

When you want to ingest *your* corpus, run the wizard.

```bash
kurious init
```

You'll be prompted for full name, work email, organization, and a project name (e.g. `q3-contracts`, `support-tickets`, `2025-handbook`). The wizard returns an API key, saves it to `~/.kurious/config.toml`, and exports `KURIOUS_API_KEY` into your shell. No browser. No copy-paste.

Then ingest:

```python
import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])
project_id = client.projects.list().projects[0].id

job = client.projects.ingest(project_id, "./my-docs/", wait=True)
print(f"Ingest {job.status}")   # 'completed' on success

result = client.search.intelligent(project_id=project_id, query="Your question here")
print(result.answer)
```

The same call accepts a single file path. Drop in `"./meeting.mp4"` and Kurious runs the full video pipeline — upload, ASR transcription, frame embeddings, captioning, indexing — in one shot. A 60-minute video is fully searchable in ~10–15 minutes. Pass `on_progress=lambda j: print(j.status)` if you want to watch.

**Formats out of the box:** PDF · DOCX · MD · TXT · PNG · JPG · MP3 · WAV · MP4 · CSV · Parquet. Pipeline auto-detected per file.

> **Builder Mode full spec:** aintropy-ai/aintropy-engine-product#675

---

## SDK reference / full docs

| | |
|---|---|
| **API docs (Swagger)** | https://kurious.aintropy.ai/api/docs |
| **SDK reference** | *Coming soon — public SDK site lands with the next release* |
| **Long-form engine guide** | Bring-your-own-data, KG, video preprocessing, production checklist |

---

## Examples

Twelve runnable scripts in [`examples/`](examples/). Each demonstrates one capability against a real demo corpus. Each is ~10–15 lines with a docstring, the call, and expected output.

| # | Script | What it shows |
|---|---|---|
| 01 | `01_hello_search.py` | Your first query — Louisville council on housing |
| 02 | `02_list_projects.py` | Every demo project you can hit |
| 03 | `03_get_project_info.py` | Look inside: file counts, formats, coverage |
| 04 | `04_search_videos.py` | Find the exact 30-second clip on a topic |
| 05 | `05_filter_by_date.py` | Same query, narrowed to Q1 2026 |
| 06 | `06_find_a_person.py` | Every mention of a speaker across hours of video |
| 07 | `07_cross_modal.py` | One query, evidence from video AND PDF |
| 08 | `08_quick_vs_deep_think.py` | Speed (`quick`) vs depth (`deep_think`) |
| 09 | `09_compare_projects.py` | Same question, two cities, side by side |
| 10 | `10_show_citations.py` | Every source span that grounded an answer |
| 11 | `11_stream_answer.py` | Stream the answer token-by-token (chat UIs) |
| 12 | `12_see_routing_decision.py` | See which pipeline ran (RAG / NL2SQL / KG) |

```bash
python examples/01_hello_search.py
```

---

## Troubleshooting / FAQ

<details>
<summary><b>I'm getting <code>401 Unauthorized</code> when installing</b></summary>

`artifacts-keyring` couldn't auto-authenticate. Get a Personal Access Token at [dev.azure.com/AIntropy-DevOps](https://dev.azure.com/AIntropy-DevOps) (avatar → Personal access tokens → scope `Packaging (Read)`). Then `export AZURE_DEVOPS_EXT_PAT="<your-PAT>"` and rerun `pip install`.
</details>

<details>
<summary><b><code>403 Forbidden</code> on a project endpoint</b></summary>

Your API key isn't scoped to that project. Trial keys work on all demo projects. `kurious init` keys are scoped to the project they were minted with.
</details>

<details>
<summary><b>I created a fresh project and search returns nothing</b></summary>

New projects default to a search mode that disables RAG. Run this once after creation:

```python
client.projects.update_config(project_id, search_mode="kg_unstructured")
```

`client.search.intelligent(...)` works regardless. Only `client.search.rag(...)` needs the mode set.
</details>

<details>
<summary><b>Ingest says <code>completed</code> but my search is empty</b></summary>

Check `client.projects.get_step_timings(project_id)`. If the `index` step has `count=0`, ingest hasn't finished writing to the search index. Give it another minute on large corpora.
</details>

<details>
<summary><b>Video search is slow on the first query</b></summary>

Cold cache. Subsequent queries hit sub-second latency. A 60-minute video takes ~10–15 minutes to fully preprocess and index.
</details>

<details>
<summary><b>Where do I report a bug?</b></summary>

[Open an issue](https://github.com/Kurious-AI/getting-started/issues/new) and pick **Bug report**. Include SDK version (`pip show aintropy`), project ID, the exact call, and the error.
</details>

---

## Roadmap

*Coming features land here next sprint.*

---

## Support

| | |
|---|---|
| **Found a bug?** | [Open an issue](https://github.com/Kurious-AI/getting-started/issues/new) |
| **Got a question? Want to share what you built?** | [GitHub Discussions](https://github.com/Kurious-AI/getting-started/discussions) or [join our Discord](https://discord.gg/aintropy-community) |
| **Need direct help?** | know@aintropy.ai |

---

## License

Apache 2.0 — see [LICENSE](LICENSE). Use it, fork it, build a company on it. We just ask you not to remove the attribution.
