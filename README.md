# Kurious — Getting Started

## Tagline

Build with Kurious, the digital and physical AI knowledge engine. From your first query to your own indexed corpus in under an hour.

---

## Introduction

Kurious is a search engine for your unstructured world — meetings, briefings, contracts, technical videos, scanned PDFs, structured tables, the messy mix of all of it. You point it at a corpus, ask a question in plain English, and it returns a grounded answer with citations back to the source span (a paragraph in a PDF, a timestamp in a video, a row in a CSV).

It runs three retrieval strategies under one API — vector + lexical RAG for unstructured documents, NL2SQL for structured tables, and a knowledge graph for multi-hop entity questions — and routes each query to the right one automatically. Same SDK, same call shape, regardless of what's in the corpus.

This repo is the fastest path from `pip install` to your first answer. Two ways in:

- **Explore Mode** — copy a trial API key out of this README, hit our demo projects, get your first answer in under a minute. No signup.
- **Builder Mode** — run `kurious init`, get your own account + project, ingest your own data.

Pick whichever fits where you are.

---

## Why Kurious

If you've shipped a RAG system before, you know the pattern: vector search, hybrid retrieval, rerank, prompt the LLM, hope the citations line up. Most of the time you're not building search — you're plumbing chunkers, embedders, vector stores, SQL routers, and OCR fallbacks into something that doesn't fall over when the next file format shows up.

Kurious replaces all of that with one API:

- **One call covers the full pipeline.** `client.projects.ingest(project_id, path)` handles upload, parsing, chunking, embedding, indexing, and (for video) ASR + frame captioning + assembly. No worker queue to operate.
- **One call covers the full retrieval surface.** `client.search.intelligent(...)` auto-routes between RAG, NL2SQL, and knowledge graph. You write the question, not the routing logic.
- **Citations come back grounded to the span.** Every answer is paired with the exact source — file + character range for documents, file + timestamp for video. No hallucinated references.
- **Mixed corpora work out of the box.** PDFs, DOCX, MP4s, CSVs in the same project, queried in the same call.
- **Hosted, multi-tenant, project-scoped.** Files, indexes, and audit logs are isolated per project. One API key per environment.

You stay focused on the use case. Kurious owns the infrastructure underneath.

---

## What can you build using Kurious?

A few patterns that show up across early customers:

- **Internal Q&A over a knowledge base** — point Kurious at your handbook, runbooks, and policy docs; wire `client.search.intelligent(...)` behind a Slack bot or web chat.
- **Meeting / call intelligence** — ingest recorded video calls; ask *"what did the customer say about renewal in March?"* and get back the exact 30-second clip.
- **Document review at scale** — drop thousands of contracts into a project, then filter by clause, party, or date range without writing custom NER.
- **Mixed-modality research agents** — combine structured filings (CSV/Parquet) with unstructured analyst reports (PDF) and earnings call recordings (MP4) in a single query.
- **Cross-corpus comparison** — run the same question across multiple municipalities, vendors, or time periods; see where answers diverge.

If you have unstructured content and a question, Kurious is a usable substrate. The examples in `examples/` show each pattern as runnable code.

---

## Prerequisites

- Python **3.10+**
- A terminal, an editor, and `pip` (or `uv` if you prefer)
- About 15 minutes for Explore Mode, 30–60 minutes for Builder Mode (depends on how much data you ingest)

That's it. No Docker, no infra to spin up, no API keys from other services.

---

## Getting started

### Step 1 — Explore Mode (your first query, no signup)

The fastest way to feel what Kurious does. You'll use a shared trial API key to query demo projects we've already indexed (Louisville city council, NJ Open Data, Seattle council, a legal video archive, ChemRAG).

**1. Install the SDK**

```bash
pip install artifacts-keyring                              # one-time, handles private feed auth
pip install "aintropy>=0.5.5,<0.6" \
  --index-url "https://pkgs.dev.azure.com/AIntropy-DevOps/Kurious-SDK/_packaging/kurious-sdk-pypi/pypi/simple/"
```

> The SDK lives on a private Azure Artifacts feed. `artifacts-keyring` handles auth transparently the first time you install. If you hit a `401`, see [Troubleshooting](#troubleshooting--faq) for the PAT fallback.

**2. Export the trial key**

```bash
export KURIOUS_API_KEY="trial_REPLACE_ME"   # placeholder — real key comes from the README when Explore Mode ships
```

**3. Run your first query**

```python
import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])

# Find the Louisville demo project
projects = client.projects.list().projects
louisville = next(p for p in projects if "louisville" in p.name.lower())

result = client.search.intelligent(
    project_id=louisville.id,
    query="What did the council decide about affordable housing?",
    mode="quick",
)
print(result.answer)
for s in result.sources[:3]:
    print(f"  {s.filename} (score={s.score:.2f})")
```

You should get an answer plus a handful of citations back from Louisville city council recordings.

That's it for Explore Mode. The `examples/` folder has ten more runnable scripts — search a video for a specific moment, filter by date, compare answers across two cities, surface citations. Each is ~15 lines, runs against the same trial key, no setup beyond Steps 1 and 2.

### Step 2 — Builder Mode (your own account + project)

When you're ready to ingest your own data, run the CLI wizard. It registers you, creates a project, and saves an API key locally.

```bash
kurious init
```

You'll be prompted for:

- Full name
- Work email
- Organization name
- A project name (e.g. `my-handbook` or `q3-contracts`)

When the wizard finishes, your API key is saved to `~/.kurious/config.toml` and exported into your current shell as `KURIOUS_API_KEY`. No browser, no copy-paste.

From there, ingest a directory:

```python
import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])
project_id = client.projects.list().projects[0].id   # the project you just created

job = client.projects.ingest(project_id, "./my-docs/", wait=True)
print(f"Indexed {job.documents_indexed} documents in {job.elapsed_s:.0f}s")

result = client.search.intelligent(project_id=project_id, query="Your question here")
print(result.answer)
```

The same call accepts a single file path. For a video, swap `"./my-docs/"` for `"./meeting.mp4"` — the SDK runs upload → ASR transcription → frame embeddings → captioning → indexing in one shot. Pass `on_progress=lambda j: print(j.status)` to watch it move through stages. Typical timing: a ~60-minute video preprocesses + indexes in ~10–15 minutes wall-clock.

Supported formats: PDF, DOCX, MD, TXT, PNG/JPG, MP3/WAV, MP4, CSV, Parquet. The pipeline (unstructured / NL2SQL / KG) is auto-detected per file.

> **Full spec for `kurious init`:** aintropy-ai/aintropy-engine-product#675

---

## SDK reference / full docs

The SDK reference (every method, every parameter) lives at:

- **API docs:** https://kurious.aintropy.ai/api/docs *(Swagger)*
- **SDK reference:** *(placeholder — link will land here once the public SDK site is up)*

For the long-form bring-your-own-data walkthrough — KG, video preprocessing, per-step monitoring, production checklist — see the canonical engine docs.

---

## Examples

Ten runnable scripts in [`examples/`](examples/), each demonstrating one Kurious capability against a real demo project. Each is ~10–15 lines with a docstring explaining the scenario, the code, and the expected output as a trailing comment.

| # | Script | What it shows |
|---|---|---|
| 01 | `01_hello_search.py` | Your first query — Louisville council on affordable housing |
| 02 | `02_list_projects.py` | What demo projects you have access to |
| 03 | `03_get_project_info.py` | Look inside a project: file counts, date range |
| 04 | `04_search_videos.py` | Find the exact timestamp where a topic was discussed |
| 05 | `05_filter_by_date.py` | Same query, narrowed to a date range |
| 06 | `06_find_a_person.py` | Find every mention of a speaker across a corpus |
| 07 | `07_cross_modal.py` | One query over both video and structured records |
| 08 | `08_quick_vs_deep_think.py` | Same query in both modes — speed vs depth tradeoff |
| 09 | `09_compare_projects.py` | Same question against Louisville and Seattle, side by side |
| 10 | `10_show_citations.py` | Every source chunk used to answer a query |

Run any of them once you've finished Step 1:

```bash
python examples/01_hello_search.py
```

---

## Troubleshooting / FAQ

**`401 Unauthorized` on install or first query**
The SDK feed needs a PAT if `artifacts-keyring` can't auto-authenticate. Get one at [dev.azure.com/AIntropy-DevOps](https://dev.azure.com/AIntropy-DevOps) → top-right avatar → Personal access tokens → scope `Packaging (Read)`. Then `export AZURE_DEVOPS_EXT_PAT="<your-PAT>"` and rerun `pip install`.

**`403 Forbidden` on a project endpoint**
Your API key isn't scoped to that project. Demo projects are accessible with the trial key; for your own projects, the key minted by `kurious init` is auto-scoped to the project it created.

**Search returns no results on a brand-new project**
Newly-created projects default to a search mode that doesn't enable RAG retrieval. After project creation:

```python
client.projects.update_config(project_id, search_mode="kg_unstructured")
```

`client.search.intelligent(...)` works on any mode; this only affects `client.search.rag(...)`.

**Ingest reports `completed` but search returns nothing**
Check `client.projects.get_step_timings(project_id)` — if the `index` step `count=0`, ingest hasn't finished writing to the search index yet. Give it another minute on large corpora.

**Video search is slow on first query**
Cold cache. Subsequent queries on the same project are sub-second. A 60-minute video takes ~25–40 minutes to preprocess end-to-end.

**How do I report a bug?**
Open an issue: https://github.com/Kurious-AI/getting-started/issues/new — pick the **Bug report** template. Include the SDK version (`pip show aintropy`), your project ID, the exact call, and the error.

---

## Roadmap

*Coming features land here next sprint.*

---

## Support

- **Found a bug?** Open an issue: https://github.com/Kurious-AI/getting-started/issues/new
- **Got a question or want to connect with the community?** [GitHub Discussions](https://github.com/Kurious-AI/getting-started/discussions) or [join our Discord](#) *(link placeholder — coming once the community Discord is live)*
- **Need direct help?** Email know@aintropy.ai

---

## License

Apache 2.0 — see [LICENSE](LICENSE).
