<div align="center">

# Kurious

**The AI knowledge engine for digital and physical AI.**  
Video, sensors, documents — cited answers in under a second.

![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?style=flat)
![SDK](https://img.shields.io/badge/aintropy-0.5.5-2ea44f?style=flat)
![License](https://img.shields.io/badge/license-Apache_2.0-blue?style=flat)
![Status](https://img.shields.io/badge/status-beta-orange?style=flat)

[Quickstart](#getting-started) · [Discord](https://discord.gg/aintropy-community) · [Discussions](https://github.com/Kurious-AI/getting-started/discussions) · [Issues](https://github.com/Kurious-AI/getting-started/issues)

</div>

```python
from aintropy import AIntropy

client = AIntropy(api_key="ak_...")
project = client.projects.create(name="My Project")

client.projects.ingest(project.id, "footage.mp4", wait=True)

result = client.search.intelligent(project.id, query="What are the key findings?")
print(result.answer)
```

---

## Introduction

Kurious is the AI knowledge engine that handles the messy work of multi-modal retrieval so you do not have to. Point the Python SDK at your data — video, sensor streams, document corpora, structured tables — and ask any question in natural language. You get back answers grounded in your source material, with every claim cited to the exact moment, page, or row it came from.

This repo is your starting point. Wire Kurious into your own data in minutes (Builder Mode).

> **Play Mode** (gate-free, no signup) — coming soon. [TBD — pending alignment]

---

## Contents

- [Why Kurious](#why-kurious)
- [What you can build](#what-you-can-build)
- [Prerequisites](#prerequisites)
- [Getting started — Builder Mode](#getting-started)
- [SDK reference](#sdk-reference)
- [Troubleshooting & FAQ](#troubleshooting--faq)
- [Roadmap](#roadmap)
- [Support](#support)

---

## Why Kurious

| | |
|---|---|
| **One SDK, every modality** | Video, sensors, documents, tables — no stitching Whisper to LangChain to Pinecone. |
| **Cited answers, not vibes** | Every response points to the exact source moment, page, or row. No fabrication. |
| **Fast and cheap** | Sub-second query latency at production cost. Numbers on our public benchmark dashboard. |
| **Cross-modal retrieval** | Ask a text question against a video. Ask a sensor question against a paper. |
| **Physical AI first-class** | Sensor streams and robot logs are core to the engine, not bolted on. |

---

## What you can build

### Beta solutions built on Kurious

| Beta | Domain | Try it |
|------|--------|--------|
| NJ Open Data | Public records, NJ municipal data | [Live demo →][URL TBD — prod URL needed] |
| Legal Videos | Legal depositions, video evidence | [Live demo →][URL TBD — prod URL needed] |
| chemRAG | Chemistry papers, lab notes | [Live demo →][URL TBD] |
| Skyfire | Drone footage and telemetry intelligence | Upcoming beta |
| Louisville | City infrastructure data | Upcoming beta |
| Enquire | (in development) | Upcoming beta |
| Zivo | (in development) | Upcoming beta |

Watch this space — upcoming betas will be linked here as they launch.

---

## Prerequisites

Four things. No Docker, no servers, no other accounts.

| | You need | How to check or get it |
|---|---|---|
| 1 | **Python 3.9 or newer** | `python --version` — download from [python.org](https://www.python.org/downloads/) if needed |
| 2 | **A terminal** | Mac: Terminal. Windows: PowerShell. Both pre-installed. |
| 3 | **Your Kurious access token** | Provided when you sign up. This unlocks the SDK download. |
| 4 | **Your data** | Video, audio, documents, images, or structured tables. Supported: `pdf`, `docx`, `txt`, `md`, `csv`, `parquet`, `png`, `jpg`, `mp3`, `wav`, `mp4`, `mov`, `mkv`, `webm` |

> [!TIP]
> Kurious does not scrape websites or transcode formats. Convert your data to a supported format before ingest.

---

## Getting started

### Builder Mode — your own data, your own API key

```mermaid
%%{init: {'flowchart': {'curve': 'basis', 'nodeSpacing': 40, 'rankSpacing': 60}}}%%
flowchart LR
    A(["<b>1</b><br/>Install"])
    B(["<b>2</b><br/>Authenticate"])
    C(["<b>3</b><br/>Create project"])
    D(["<b>4</b><br/>Ingest"])
    E(["<b>5</b><br/>Search"])

    A --> B --> C --> D --> E

    classDef step fill:#0969da,stroke:#0969da,color:#ffffff,stroke-width:2px
    classDef finish fill:#2da44e,stroke:#2da44e,color:#ffffff,stroke-width:2px
    class A,B,C,D step
    class E finish
    linkStyle default stroke:#8b949e,stroke-width:2px
```

> **Play Mode** — want to try Kurious without signing up first? Coming soon. [TBD — placeholder]

---

### Step 1 — Install the SDK

```bash
export KURIOUS_TOKEN="<your-access-token>"

pip install "aintropy==0.5.5" \
  --index-url "https://aintropy:${KURIOUS_TOKEN}@pkgs.dev.azure.com/AIntropy-DevOps/Kurious-SDK/_packaging/kurious-sdk-pypi/pypi/simple/" \
  --extra-index-url "https://pypi.org/simple/"
```

Verify:

```bash
python -c "import aintropy; print(aintropy.__version__)"
# Expected: 0.5.5
```

> [!WARNING]
> Hit `401 Unauthorized`? Your access token is missing or wrong. Re-export it and rerun. Confirm the token has **Packaging (Read)** scope.

---

### Step 2 — Authenticate

Sign up at **[TBD — prod signup URL]** to get your API key. Then:

```python
from aintropy import AIntropy

client = AIntropy(api_key="your_api_key_here")
```

That is the full auth step. One line.

---

### Step 3 — Create a project

```python
project = client.projects.create(
    name="my-first-project",
    description="My Kurious project",
)
PROJECT_ID = project.id
print(f"Project ID: {PROJECT_ID}")
```

> [!IMPORTANT]
> Run this one extra line right after creating a new project:
> ```python
> client.projects.update_config(PROJECT_ID, search_mode="kg_unstructured")
> ```
> Without it, `client.search.rag(...)` returns zero results even when your files are indexed correctly. Single most common gotcha.

---

### Step 4 — Ingest your data

```python
import time

job = client.projects.ingest(
    PROJECT_ID,
    "/path/to/your/file.mp4",   # video, doc, image, or structured data
    wait=True,
    on_progress=lambda j: print(f"  status={j.status}"),
)
print(f"Done — status: {job.status}")
```

**How long it takes:** roughly one minute of processing per ten minutes of video. Documents finish in seconds. You only run this once per file.

> [!TIP]
> `status` says `completed` but search returns nothing? Give it another minute — indexing runs after preprocessing. If it is still empty, check that you ran `update_config` in Step 3.

---

### Step 5 — Run your first search

```python
# Grounded answer with citations
result = client.search.intelligent(PROJECT_ID, "your question here")
print(result.answer)
for source in result.sources:
    print(f"  - {source}")
```

```python
# Raw hits with timestamps and source locations (requires search_mode="kg_unstructured")
hits = client.search.rag(PROJECT_ID, query="your question here", limit=5)
for h in hits.hits:
    print(h)
```

**Example questions that show Kurious at its best:**

- `"At what timestamp did the speaker first mention the damages clause?"` — legal video
- `"Show me all moments in the footage where a person is near a vehicle"` — drone footage
- `"What do the sensor logs show in the 30 seconds before the anomaly?"` — infrastructure data

> [!TIP]
> Kurious only returns evidence-backed answers. If supporting evidence is not in your data, it will say so rather than fabricate a response. Spot-check your first results — open the cited source at the cited location to confirm.

---

## SDK reference

| Method | What it does |
|--------|-------------|
| `client.projects.create(name, description)` | Create a new project (isolated index) |
| `client.projects.ingest(project_id, path, wait=True)` | Upload and index a file or folder |
| `client.search.intelligent(project_id, query)` | Natural-language answer with cited sources |
| `client.search.rag(project_id, query, limit)` | Raw matching chunks with scores and timestamps |

**Full SDK docs:** [docs.kurious.aintropy.ai](https://docs.kurious.aintropy.ai) *(coming soon)*

---

## Troubleshooting & FAQ

<details>
<summary><b>My query returns no citations.</b></summary>
<br>
Either the question is too broad, or the project does not contain relevant data. Try narrowing to the modality you expect — for example: "in the video footage, when did..." or "in the sensor logs, where did...". Kurious only returns evidence-backed answers and will not fabricate a citation.
</details>

<details>
<summary><b>My ingest is slower than expected.</b></summary>
<br>
Video is the most computationally intensive modality and scales with duration. Roughly one minute of processing per ten minutes of video on the trial cluster. If you need faster ingest, contact us at know@aintropy.ai.
</details>

<details>
<summary><b>The API key is rate-limited.</b></summary>
<br>
Trial keys are intentionally rate-limited for evaluation, not production workloads. If you hit the limit, contact know@aintropy.ai to discuss higher limits.
</details>

<details>
<summary><b>Where does Kurious get its data from?</b></summary>
<br>
Kurious never invents knowledge. Every answer comes directly from the data sources you provide during ingestion — video timestamps, sensor events, document passages, or structured table rows.
</details>

<details>
<summary><b>Something is broken. How do I report it?</b></summary>
<br>
Open a new issue using the Bug report template in this repo. It auto-prompts for SDK version, modality, the call you made, and what you saw vs expected. We aim to triage every bug within one business day.
</details>

---

## Roadmap

> **[TBD — to be updated next sprint]**

---

## Support

> **[TBD — Shivangi to update with GitHub Issues, GitHub Discussions, Discord, know@aintropy.ai]**

---

## License

Apache 2.0 — see [LICENSE](LICENSE).
