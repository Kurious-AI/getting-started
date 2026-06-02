<div align="center">

# Kurious

**The AI knowledge engine for Digital and Physical AI.**

Cross-modal retrieval across video, sensors, documents, and structured tables. Grounded citations. Sub-second latency. One SDK call.

![Python](https://img.shields.io/badge/python-3.12%2B-3776AB?style=flat)
![SDK](https://img.shields.io/badge/aintropy-0.5.5-2ea44f?style=flat)
![License](https://img.shields.io/badge/license-Apache_2.0-blue?style=flat)
![Status](https://img.shields.io/badge/status-beta-orange?style=flat)

[Quickstart](#getting-started) · [Discord](https://discord.gg/aintropy-community) · [Discussions](https://github.com/Kurious-AI/getting-started/discussions) · [Issues](https://github.com/Kurious-AI/getting-started/issues)

</div>

---

## Contents

- [What you'll build](#what-youll-build)
- [Prerequisites](#prerequisites)
- [Install the SDK](#install-the-sdk)
- [Getting started](#getting-started)
  - [Step 1. Point at your file](#step-1-of-5-point-at-your-file)
  - [Step 2. Sign in and get an API key](#step-2-of-5-sign-in-and-get-an-api-key)
  - [Step 3. Create your project](#step-3-of-5-create-your-project)
  - [Step 4. Load your file](#step-4-of-5-load-your-file-into-the-project)
  - [Step 5. Run your first search](#step-5-of-5-run-your-first-search)
- [SDK reference](#the-sdk-in-two-commands)
- [Troubleshooting & FAQ](#troubleshooting--faq)
- [Support](#support)

---

## What you'll build

By the end of this guide you'll have:

- The Kurious Python SDK installed and authenticated.
- A project that holds one indexed file (video, audio, document, image, or structured table).
- A working `client.search.rag(...)` call that returns grounded, cited hits.

Total time: about 15 minutes for documents, 25 minutes if you're indexing a 60-minute video.

---

## Prerequisites

Four things, no Docker, no servers, no other accounts.

| | You need | How to check or get it |
|---|---|---|
| 1 | **Python 3.12 or newer** | Open your terminal and run `python --version`. If you do not have it, download from [python.org](https://www.python.org/downloads/). |
| 2 | **A terminal app** | Mac: Terminal. Windows: PowerShell. Both come pre-installed. |
| 3 | **Your Aintropy access token (PAT)** | Aintropy emails you a Personal Access Token. This is what unlocks the SDK download. |
| 4 | **A multimodal knowledge source** | Video, audio, documents, images, or structured tables you want Kurious to index into one queryable semantic layer. Mix freely in one project. Supported formats: `pdf`, `docx`, `txt`, `md`, `csv`, `parquet`, `png`, `jpg`, `mp3`, `wav`, `mp4`, `mov`, `mkv`, `webm`. |

> [!TIP]
> Kurious does not scrape websites or transcode formats. Convert your data to one of the supported formats before ingest.

<br>

---

## Install the SDK

Four commands. Run them one at a time, waiting for each to finish.

#### 1. Set your access token

```bash
export AZURE_DEVOPS_TOKEN="<paste your PAT here>"
```

#### 2. Install Kurious

```bash
pip install --upgrade "aintropy==0.5.5" \
  --index-url "https://aintropy:${AZURE_DEVOPS_TOKEN}@pkgs.dev.azure.com/AIntropy-DevOps/Kurious-SDK/_packaging/kurious-sdk-pypi/pypi/simple/" \
  --extra-index-url "https://pypi.org/simple/"
```

#### 3. Install two helpers used later

```bash
pip install jupyter requests
```

#### 4. Verify

```bash
python -c "import aintropy; print(aintropy.__version__)"
```

Expected output: `0.5.5`

> [!WARNING]
> **Hit `401 Unauthorized`?** Your `AZURE_DEVOPS_TOKEN` is missing or wrong. Re-export it and rerun the install. If the token is still rejected, check that it has the **Packaging (Read)** scope.

<br>

---

## Getting started

Five steps from zero to a working search.

```mermaid
%%{init: {'flowchart': {'curve': 'basis', 'nodeSpacing': 40, 'rankSpacing': 60}}}%%
flowchart LR
    A(["<b>1</b><br/>Pick a file"])
    B(["<b>2</b><br/>Sign in"])
    C(["<b>3</b><br/>Create project"])
    D(["<b>4</b><br/>Load file"])
    E(["<b>5</b><br/>Search"])

    A --> B --> C --> D --> E

    classDef step fill:#0969da,stroke:#0969da,color:#ffffff,stroke-width:2px
    classDef finish fill:#2da44e,stroke:#2da44e,color:#ffffff,stroke-width:2px
    class A,B,C,D step
    class E finish
    linkStyle default stroke:#8b949e,stroke-width:2px
```

<br>

### Step 1 of 5. Point at your file

**Goal:** tell Python where the file you want to index lives on disk.

```python
import os

FILE_PATH    = os.path.expanduser("~/Desktop/my_video.mp4")   # replace
PROJECT_NAME = "my-first-project"                              # replace

assert os.path.isfile(FILE_PATH), f"FILE_PATH does not exist: {FILE_PATH}"
size_mb = os.path.getsize(FILE_PATH) / (1024 * 1024)
print(f"  file: {FILE_PATH}")
print(f"  size: {size_mb:.1f} MB")
```

If you see an `AssertionError`, the path is wrong. Fix it and rerun.

<br>

---

### Step 2 of 5. Sign in and get an API key

**Goal:** create your account (or log in), mint an API key scoped to your company, and build the `client` object you'll use for the rest of the tutorial.

Behind the scenes this is three calls: a `signup`/`login` for a short-lived JWT, an `/api-keys/create` to exchange the JWT for a long-lived API key, and the SDK client construction.

> [!TIP]
> Already have a working `client` from earlier in this session? Skip Step 2. The same object works for the rest of the tutorial.

```python
import requests
from aintropy import AIntropy

BASE_URL  = "https://kurious-backend-dev-api.centralus.cloudapp.azure.com/api/v1"
USERS_URL = "https://kurious-backend-dev-api.centralus.cloudapp.azure.com/users"

TEST_EMAIL     = "you@yourcompany.com"   # replace
TEST_PASSWORD  = "YourStrongPassword!"   # replace
TEST_FULL_NAME = "Your Name"             # replace
TEST_COMPANY   = "your-company"          # replace

# Signup, or fall back to login if the account already exists
r = requests.post(
    f"{USERS_URL}/auth/signup",
    json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "full_name": TEST_FULL_NAME,
        "company_name": TEST_COMPANY,
    },
    timeout=30,
)
if r.status_code == 409:   # account already exists, log in instead
    r = requests.post(
        f"{USERS_URL}/auth/login",
        json={"username": TEST_EMAIL, "password": TEST_PASSWORD},
        timeout=30,
    )
r.raise_for_status()
tokens = r.json()
print(f"  JWT: {tokens['access_token'][:16]}...")

# Exchange the JWT for a longer-lived API key + your company ID
r = requests.post(
    f"{BASE_URL}/api-keys/create",
    headers={
        "Authorization": f"Bearer {tokens['access_token']}",
        "Content-Type": "application/json",
    },
    json={
        "name": "my-first-key",
        "access_type": "read_write",
        "max_index": 10,
        "max_size_gb": 5.0,
        "expiry_days": 7,
    },
    timeout=30,
)
r.raise_for_status()
k = r.json()
api_key, company_id = k["api_key"], k["company_id"]
print(f"  API key: {api_key[:12]}... company={company_id}")

# Build the SDK client and attach your company ID to every request
client = AIntropy(api_key=api_key, base_url=BASE_URL)
_orig = client._transport._build_headers
def _with_cid(extra=None, _o=_orig, _c=company_id, **kw):
    h = _o(extra, **kw)
    h.setdefault("X-Company-ID", _c)
    return h
client._transport._build_headers = _with_cid
print("  client ready")
```

> [!NOTE]
> **`409 Conflict` on signup is expected.** It just means the email already has an account. The Step 2 code falls back to login automatically. Nothing to fix.

**Fields you can set on `api-keys/create`:**

| Field | What it means |
|---|---|
| `name` | A label for this key. |
| `access_type` | `read_write` lets you upload files. `read_only` only allows searching. |
| `max_index` | How many projects this key can access. |
| `max_size_gb` | Total storage this key can use. |
| `expiry_days` | How long the key stays valid. |

> [!TIP]
> **Set `max_index` and `max_size_gb` to fit your expected corpus.** At default chunking, ~1,000 hours of video lands around 100 GB of storage.

<br>

---

### Step 3 of 5. Create your project

**Goal:** spin up an isolated semantic index that will hold your file. One project per corpus.

```python
lst = client.projects.list(skip=0, limit=50)
project = next((p for p in lst.projects if p.name == PROJECT_NAME), None)
if project is None:
    project = client.projects.create(
        name=PROJECT_NAME,
        description="My first Kurious project",
    )
PROJECT_ID = project.id
print(f"  PROJECT_ID = {PROJECT_ID}")
```

The code reuses an existing project if one with this name exists, otherwise creates a new one.

> [!IMPORTANT]
> **Run this one extra line right after creating a new project:**
> ```python
> client.projects.update_config(PROJECT_ID, search_mode="kg_unstructured")
> ```
> Without it, `client.search.rag(...)` returns zero results even when your files are loaded correctly. **Single most common gotcha in this tutorial.** `client.search.intelligent(...)` is not affected.

> [!TIP]
> **Search runs inside one project at a time.** For cross-project retrieval, either query each project separately, or load every source into one project and filter by provenance at query time.

<br>

---

### Step 4 of 5. Load your file into the project

**Goal:** upload and index your file. One call covers parsing, transcription, frame analysis (for video), captioning, and indexing.

```python
import time

t0 = time.time()
job = client.projects.ingest(
    PROJECT_ID,
    FILE_PATH,
    wait=True,
    on_progress=lambda j: print(f"  [{time.time()-t0:7.1f}s] status={j.status}"),
)
print(f"\nDONE in {time.time()-t0:.0f}s  ·  job.id={job.id}  ·  status={job.status}")
```

The `on_progress` callback prints live status updates so you know the call is still working.

**How long it takes**

A 60-minute video takes about 9 minutes total (roughly 7 minutes of preprocessing plus 80 seconds of indexing). Documents and shorter formats finish faster. You only run this once per file.

> [!TIP]
> **`status` says `completed` but search returns nothing?** Inspect the underlying job directly:
> ```python
> import requests
> s = requests.get(
>     f"{BASE_URL}/jobs/{job.id}",
>     headers=client._transport._build_headers(),
>     timeout=15,
> ).json()
> print(f"  status            : {s.get('status')}")
> print(f"  documents_indexed : {s.get('result', {}).get('documents_indexed')}")
> ```
> If `status` is `running`, give it another minute. If `documents_indexed` is `0`, something went wrong during indexing.

> [!TIP]
> **Loading many files at once?** Use `wait=False` and a Python loop to dispatch jobs without blocking:
> ```python
> jobs = [client.projects.ingest(PROJECT_ID, path, wait=False) for path in paths]
> # then poll for completion
> ```
> Concurrent ingests share GPU capacity on the backend, so even parallel calls run partly serially.

<br>

---

### Step 5 of 5. Run your first search

**Goal:** ask a natural-language question and get back grounded hits with timestamps, character ranges, and source URLs.

```python
import time

queries = [
    "What is the main argument in this content?",
    "What are the next steps mentioned?",
]

for q in queries:
    print(f"\nQ: {q}")
    t0 = time.perf_counter()
    res = client.search.rag(PROJECT_ID, query=q, limit=5)
    latency_ms = (time.perf_counter() - t0) * 1000
    print(f"  -> {res.hit_count} hits in {latency_ms:.0f} ms")

    for i, h in enumerate(res.hits[:3], 1):
        score    = h.get("_score") or h.get("score") or h.get("relevance_score")
        text     = h.get("text") or h.get("content") or h.get("excerpt") or ""
        url      = h.get("video_url") or h.get("source_url") or h.get("url") or h.get("document_url")
        start_ms = h.get("start_ms")
        end_ms   = h.get("end_ms")
        chunk_id = h.get("chunk_id") or h.get("_id") or h.get("doc_uuid")
        preview  = str(text).replace("\n", " ")[:240]

        print(f"  [{i}] score={score}  time={start_ms}-{end_ms}ms  chunk_id={chunk_id}")
        print(f"      text: {preview}")
        if url:
            print(f"      url:  {url}")
```

For every hit, you'll see the matching text, the relevance score, the source URL, and either timestamps (for video and audio) or character ranges (for documents).

> [!TIP]
> **Hit field names vary by modality.** Score may live at `_score`, `score`, or `relevance_score`. Text at `text`, `content`, or `excerpt`. URLs at `video_url`, `source_url`, `url`, or `document_url`. Always read with `.get()` and fallbacks so your code works across modalities.

> [!IMPORTANT]
> **Spot-check your first results.** Open the cited source at the cited location and confirm the text matches. For video, jump to the timestamp. For a document, open the file at the character range. Grounded citations are Kurious's strongest guarantee; verifying once is how you build trust in your project.

<br>

---

## The SDK in two commands

After setup, almost everything you do uses one of these two.

```mermaid
%%{init: {'flowchart': {'curve': 'basis', 'nodeSpacing': 40, 'rankSpacing': 60}}}%%
flowchart LR
    A(["<b>ingest&#40;&#41;</b><br/>once per file"])
    B[("Project<br/>ready")]
    C(["<b>search&#40;&#41;</b><br/>any number of times"])
    D(["<b>Cited answer</b><br/>timestamps, spans, rows"])

    A --> B --> C --> D

    classDef cmd fill:#0969da,stroke:#0969da,color:#ffffff,stroke-width:2px
    classDef state fill:#bf8700,stroke:#bf8700,color:#ffffff,stroke-width:2px
    classDef result fill:#2da44e,stroke:#2da44e,color:#ffffff,stroke-width:2px
    class A,C cmd
    class B state
    class D result
    linkStyle default stroke:#8b949e,stroke-width:2px
```

#### Load files

```python
client.projects.ingest(project_id, path, wait=True)
```

Pass a folder or a single file. Returns a job object with `job.status` and `job.id`. Run once per file.

#### Search

| Method | Returns | Use when |
|---|---|---|
| `client.search.rag(...)` | Raw matching chunks with scores, timestamps, and source URLs | You want raw hits for a custom UI or downstream code. Requires `search_mode="kg_unstructured"`. |
| `client.search.intelligent(...)` | Written answer plus cited sources | You want a finished, grounded answer to surface to a user. Works on either search mode. |

<br>

---

## Troubleshooting & FAQ

<details>
<summary><b>My data isn't being ingested or scraped correctly.</b></summary>

<br>

Kurious supports a wide range of modalities including video, sensor streams, documents, structured tables, and multimodal datasets.

If your data format is unusual or highly specialized, reach out and we'll help determine the best ingestion path.

Contact: [help@aintropy.ai](mailto:help@aintropy.ai)

</details>

<details>
<summary><b>My query returns no citations.</b></summary>

<br>

Either the question is too broad, or the project does not contain relevant data.

Try narrowing the question to the modality you expect:

- *"in the video footage, when did..."*
- *"in the sensor logs, where did..."*

Kurious only returns evidence-backed answers. If supporting evidence cannot be found, it will not fabricate a citation.

</details>

<details>
<summary><b>Where does Kurious get its data from?</b></summary>

<br>

Kurious never invents knowledge. Every answer comes directly from the data sources you provide during ingestion.

Depending on your project, citations may point back to:

- Video timestamps
- Sensor events
- Robot logs
- Document passages
- Structured table rows

Every answer remains grounded in your source material.

</details>

<details>
<summary><b>Where do the demo videos and legal datasets come from?</b></summary>

<br>

The demo projects included in Kurious use publicly available datasets and example content intended for evaluation and experimentation. Production deployments use customer-provided data.

</details>

<details>
<summary><b><code>kurious init</code> hangs at the email step.</b></summary>

<br>

Email verification is sent through a one-time login link. Check your inbox and spam folder. If nothing arrives within five minutes, file a bug report.

</details>

<details>
<summary><b>My ingest is slower than expected.</b></summary>

<br>

Video is the most computationally intensive modality and processing time scales with duration. As a rough guideline, trial infrastructure processes approximately ten minutes of video per minute of ingest time.

Builder Mode customers can request faster ingestion configurations through paid infrastructure tiers.

</details>

<details>
<summary><b>The trial API key is rate limited.</b></summary>

<br>

Yes, intentionally. Explore Mode is designed for evaluation, not production workloads.

If you hit limits, run:

```bash
kurious init
```

to switch into Builder Mode using your own API key and higher limits.

</details>

<details>
<summary><b>Something is broken or behaving unexpectedly. How do I report it?</b></summary>

<br>

Open a new issue using the Bug Report template in this repository. The template automatically captures:

- SDK version
- Modality
- Request details
- Expected behavior
- Actual behavior

Our goal is to triage and tag all reported bugs within one business day.

</details>

<br>

---

## Resources

| | |
|---|---|
| **API reference** | [kurious.aintropy.ai/api/docs](https://kurious.aintropy.ai/api/docs) |
| **SDK reference** | Coming soon |
| **Long-form guide** | See the engine guide |

---

## Support

- **Found a bug?** [Open an issue](https://github.com/Kurious-AI/getting-started/issues/new), pick **Bug report**, and include your SDK version (`pip show aintropy`), the project ID, the call you ran, and the error message.
- **Question or show-and-tell?** [Discussions](https://github.com/Kurious-AI/getting-started/discussions) or [Discord](https://discord.gg/aintropy-community).
- **Direct help:** [know@aintropy.ai](mailto:know@aintropy.ai).

---

## License

Apache 2.0. See [LICENSE](LICENSE).
