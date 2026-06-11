<div align="center">

<a href="https://aintropy.ai"><img src="assets/logo.png" width="120" alt="AIntropy" /></a>

# Kurious

**The AI knowledge engine for digital and physical AI.**  
Video, sensors, documents — cited answers in under a second.

![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?style=flat)
![SDK](https://img.shields.io/badge/kurious-0.8.0-2ea44f?style=flat)
![License](https://img.shields.io/badge/license-Apache_2.0-blue?style=flat)
![Status](https://img.shields.io/badge/status-beta-orange?style=flat)
[![Discord](https://img.shields.io/badge/Discord-join-5865F2?style=flat&logo=discord&logoColor=white)](https://discord.gg/aintropy-community)
[![GitHub Discussions](https://img.shields.io/badge/GitHub-discussions-181717?style=flat&logo=github)](https://github.com/Kurious-AI/getting-started/discussions)

[Quickstart](#getting-started) · [Discord](https://discord.gg/aintropy-community) · [Discussions](https://github.com/Kurious-AI/getting-started/discussions) · [Issues](https://github.com/Kurious-AI/getting-started/issues)

</div>

```python
from kurious import Kurious

client = Kurious(api_key="ak_...")
project = client.projects.create(name="My Project")

client.projects.ingest(project.id, "footage.mp4", wait=True)

result = client.search.intelligent(project.id, query="What are the key findings?")
print(result.answer)
```

---

## Introduction

Kurious is the AI knowledge engine that handles the messy work of multi-modal retrieval so you do not have to. Point the SDK at your data, ask a question in plain English, get a cited answer. This repo gets you there in minutes.

---

## Contents

- [Why Kurious](#why-kurious)
- [What you can build](#what-you-can-build)
- [Prerequisites](#prerequisites)
- [Getting started — Builder Mode](#getting-started)
- [SDK reference](#sdk-reference)
- [Troubleshooting & FAQ](#troubleshooting--faq)
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
| NJ Open Data | Public records, NJ municipal data | Coming soon |
| Legal Videos | Legal depositions, video evidence | Coming soon |
| chemRAG | Chemistry papers, lab notes | Coming soon |
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
| 3 | **A Kurious account** | Created in seconds from your terminal in [Step 2](#step-2--authenticate) — no browser needed. *(Package-install authentication is being finalized — see the note in [Step 1](#step-1--install-the-sdk).)* |
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

> **Play Mode** — want to try Kurious without signing up first? Coming soon.

---

### Step 1 — Install the SDK

```bash
pip install "kurious==0.8.0" \
  --index-url "https://pkgs.dev.azure.com/AIntropy-DevOps/Kurious-SDK/_packaging/kurious-sdk-pypi/pypi/simple/"
```

Verify:

```bash
python -c "import kurious; print(kurious.__version__)"
# Expected: 0.8.0
```

> [!NOTE]
> **Install authentication — coming soon.** The exact steps for authenticating to the
> package feed are being finalized. If `pip install` fails with `401 Unauthorized`, the
> feed credentials aren't published yet — check back shortly.

<!-- TODO(eng): finalize package-feed auth before this repo goes public. Pending decision — publish `kurious` to public PyPI (no install token) vs. issue a packaging token at signup. Tracking: aintropy-engine-product issue (TBD, filed by Shivangi). -->

---

### Step 2 — Authenticate

One command. No browser, no dashboard — `kurious init` creates your account and API key right from the terminal:

```bash
kurious init
# Enter your email: you@example.com
# Enter the code we just emailed you: 123456
# ✅ Account ready. API key saved to ~/.kurious/config.toml
```

Then load it automatically in your code — no keys to copy or paste:

```python
from kurious import Kurious

client = Kurious.from_config()
```

`from_config()` reads the API key that `kurious init` saved for you.

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

> [!TIP]
> Ingesting a long video and don't want to block? Use `wait="background"` to get the job handle back immediately, then poll on your own schedule:
> ```python
> job = client.projects.ingest(PROJECT_ID, "/path/to/file.mp4", wait="background")
> job.wait_until_running()   # returns once a worker picks up the job
> # later, check on it: job.refresh(); print(job.status)
> ```

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
| `client.projects.ingest(project_id, path, wait=True)` | Upload and index a file or folder (use `wait="background"` to return immediately) |
| `client.search.intelligent(project_id, query)` | Natural-language answer with cited sources |
| `client.search.rag(project_id, query, limit)` | Raw matching chunks with scores and timestamps |
| `client.entitlements.get(company_id)` | Read your current plan type and request quota |

**Full SDK docs:** [docs.kurious.aintropy.ai](https://docs.kurious.aintropy.ai) *(coming soon)*

---

## Troubleshooting & FAQ

<details>
<summary><b>The SDK threw a TimeoutError during ingest. Did my job fail?</b></summary>
<br>
No. <code>TimeoutError</code> is a client-side timeout — your backend job is still running. The file is still being processed on the server. Wait a few minutes, then check status:

```python
files = client.files.list(PROJECT_ID)
for f in files.files:
    print(f.filename, f.status)
```

Do not re-ingest. Once status shows <code>indexed</code>, run your search.
</details>

<details>
<summary><b>Ingest completed but search returns 0 sources.</b></summary>
<br>
Two likely causes:

1. **Indexing lag** — indexing runs after preprocessing finishes. Wait 1–2 minutes after ingest completes, then search again.
2. **Missing update_config** — if you skipped this step after creating the project, `search.rag()` will always return empty. Run:

```python
client.projects.update_config(PROJECT_ID, search_mode="kg_unstructured")
```

Then search again.
</details>

<details>
<summary><b>Search returned 0 results immediately after ingest timed out.</b></summary>
<br>
If you set a <code>timeout_s</code> and the SDK timed out, your file may still be ingesting on the backend — the job did not fail, it just kept running after the client disconnected. Check <code>client.files.list(PROJECT_ID)</code>. If status is <code>ingesting</code>, wait for it to reach <code>indexed</code> before searching.
</details>

<details>
<summary><b>My on_progress callback shows stage=None the whole time.</b></summary>
<br>
Known limitation — pipeline stage visibility is not yet surfaced in the SDK response. Your job is still running. Monitor wall-clock time rather than stage output.
</details>

<details>
<summary><b>How long does ingest take?</b></summary>
<br>
It depends on the modality:

- **Video:** roughly 1 minute of processing per 10 minutes of footage. A 100 MB file (~10 min) takes 15–40 minutes on the trial cluster.
- **Documents (PDF, DOCX, TXT):** seconds to a few minutes depending on size.
- **Images and structured data:** seconds.

You only need to ingest each file once.
</details>

<details>
<summary><b>The API key is rate-limited.</b></summary>
<br>
Trial keys are intentionally rate-limited for evaluation, not production workloads. Check your current plan and daily quota anytime:

```python
ent = client.entitlements.get(company_id)
print(ent.plan_type, ent.requests_per_day)
```

If you hit the limit, contact know@aintropy.ai to discuss higher limits.
</details>

<details>
<summary><b>Where does Kurious get its data from?</b></summary>
<br>
Kurious never invents knowledge. Every answer comes directly from the data sources you provide during ingestion — video timestamps, sensor events, document passages, or structured table rows. If the evidence is not in your data, Kurious says so.
</details>

<details>
<summary><b>Something is broken. How do I report it?</b></summary>
<br>
Open a new issue using the Bug report template in this repo. It prompts for SDK version, modality, the exact call you made, and what you saw vs expected. We aim to triage every bug within one business day.
</details>

---

## Support

- **Bug reports:** [Open an issue](https://github.com/Kurious-AI/getting-started/issues/new/choose) — the bug report template prompts for everything we need.
- **Email:** know@aintropy.ai

---

## License

Apache 2.0 — see [LICENSE](LICENSE).
