<div align="center">

# Kurious

**Take a multimodal corpus from local disk to a queryable index, using only the public SDK.**

[Quickstart](#getting-started) · [Discord](https://discord.gg/aintropy-community) · [Discussions](https://github.com/Kurious-AI/getting-started/discussions)

</div>

---

## What is Kurious

One tool that reads all your unstructured content (PDFs, Word docs, spreadsheets, audio, video) and answers questions in plain English. Every answer links back to the exact source span (page and character range for documents, start and end timestamps for video).

You skip the database, the embedder, the chunker, the transcription pipeline, and the citation glue. You write the question.

---

## Why Kurious

| Without Kurious | With Kurious |
|---|---|
| Pick a database, a model, a chunker. Wire them up. Maintain them. | One package. A few lines of code. |
| Separate code paths for documents, spreadsheets, and video. | One call covers all formats. |
| Bolt on OCR, transcription, and frame analysis. | One ingest pipeline handles them. |
| Build citations from scratch. | Citations by default. |
| Run and scale servers. | Hosted. |

---

## What you can build

- **Internal Q&A.** *"What is our PTO policy for new hires?"*
- **Meeting search.** *"What did the customer say about renewal in March?"*
- **Contract review at scale.** *"Which contracts mention exclusivity?"*
- **Cross-format research.** Combine filings, analyst PDFs, and earnings call recordings in one project.
- **Side-by-side comparison.** Same question, twenty cities. See where they differ.

---

## Prerequisites

| You need | How to check or get it |
|---|---|
| **Python 3.12 or newer** | Run `python --version` in your terminal. If you do not have it, download from [python.org](https://www.python.org/downloads/). |
| **A terminal app** | Mac: Terminal. Windows: PowerShell. Both come pre-installed. |
| **Your Aintropy access token (PAT)** | Aintropy emails you a Personal Access Token. This is what unlocks the SDK download. |
| **Your test account** | An email, password, full name, and company name you will use to sign up against the Kurious backend. |
| **A file to search** | Any PDF, Word doc, spreadsheet, image, audio, or video file on your computer. For video: `mp4`, `mov`, `mkv`, or `webm`. |

> [!NOTE]
> No Docker. No servers. No other accounts. The SDK installs through `pip` like any Python package.

---

## Install the SDK

Open your terminal. Paste your access token into the first command, replacing the placeholder. Then run the install.

```bash
export AZURE_DEVOPS_TOKEN="<paste your PAT here>"
```

```bash
pip install --upgrade "aintropy==0.5.5" \
  --index-url "https://aintropy:${AZURE_DEVOPS_TOKEN}@pkgs.dev.azure.com/AIntropy-DevOps/Kurious-SDK/_packaging/kurious-sdk-pypi/pypi/simple/" \
  --extra-index-url "https://pypi.org/simple/"
```

```bash
pip install jupyter requests
```

**Verify it worked:**

```bash
python -c "import aintropy; print(aintropy.__version__)"
```

You should see `0.5.5` printed. If you do, the SDK is ready.

> [!TIP]
> Hit `401 Unauthorized`? Your token is missing or wrong. Re-export `AZURE_DEVOPS_TOKEN` and try again.

---

## Getting started

Five steps from zero to a working query.

```mermaid
flowchart LR
    A[1. Pick a file] --> B[2. Sign in<br/>+ get API key] --> C[3. Create<br/>a project] --> D[4. Ingest] --> E[5. Search]
```

---

### Step 1. Point at your file

```python
import os

FILE_PATH    = os.path.expanduser("~/Desktop/my_video.mp4")   # replace with your file
PROJECT_NAME = "my-first-project"                              # replace with your project name

assert os.path.isfile(FILE_PATH), f"FILE_PATH does not exist: {FILE_PATH}"
size_mb = os.path.getsize(FILE_PATH) / (1024 * 1024)
print(f"  file: {FILE_PATH}")
print(f"  size: {size_mb:.1f} MB")
```

The `os.path.expanduser` part turns `~` into your home folder so the path works on any computer.

---

### Step 2. Sign in and get an API key

Kurious uses two endpoints to set up your session:

1. **Users service** for signup or login. Returns a short-lived JWT (a temporary login token).
2. **API keys service** to mint a long-lived API key from the JWT.

Then you wrap both in the `AIntropy(...)` client.

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

> [!IMPORTANT]
> The last block (`_with_cid`) tells the SDK to attach your `company_id` to every request. The Kurious backend currently requires this header. Copy the block as-is. You only run this once per session.

**What `api-keys/create` accepts:**

| Field | What it means |
|---|---|
| `name` | A label for this key. Anything you want. |
| `access_type` | `read_write` or `read_only`. |
| `max_index` | How many projects this key can use. |
| `max_size_gb` | Total storage this key can occupy. |
| `expiry_days` | How long the key stays valid. |

---

### Step 3. Create (or reuse) a project

A **project** is a named container for one set of files. You can have many projects, for example one for your handbook and one for your contracts. Search runs inside one project at a time.

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

This first asks Kurious for projects that already exist. If yours is there, reuse it. Otherwise create it.

> [!IMPORTANT]
> Run this once right after creating a new project:
> ```python
> client.projects.update_config(PROJECT_ID, search_mode="kg_unstructured")
> ```
> New projects default to `search_mode="unstructured"`. With that default, `client.search.rag(...)` silently returns zero hits even when your files are correctly loaded. This is the most common gotcha. `client.search.intelligent(...)` is not affected.

---

### Step 4. Ingest your file

One call covers everything: upload, parsing, transcription (for audio and video), frame analysis (for video), captioning, and indexing.

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

The `on_progress` callback prints status updates while Kurious works.

**What happens inside this call:**

1. Your file uploads to Kurious
2. The pipeline auto-detects the file type
3. For documents: text is parsed and chunked
4. For audio and video: speech is transcribed
5. For video: frames are analyzed and captioned
6. Everything is indexed so you can search it

**How long it takes:**

| Content type | Roughly |
|---|---|
| Documents (PDF, DOCX, CSV, etc.) | Seconds |
| Audio | 1 to 2 minutes per hour |
| Video | About 9 minutes per hour (preprocess ~7 min + indexing ~80s for a 60-minute video) |

You only run this once per file.

---

### Step 5. Search

```python
import time

# Replace these with questions that match the content you loaded
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
        score    = h.get("_score") or h.get("score")
        text     = h.get("text") or h.get("content") or h.get("excerpt") or ""
        url      = h.get("video_url") or h.get("source_url") or h.get("url")
        start_ms = h.get("start_ms")
        end_ms   = h.get("end_ms")
        chunk_id = h.get("chunk_id") or h.get("_id")
        preview  = str(text).replace("\n", " ")[:240]

        print(f"  [{i}] score={score}  time={start_ms}-{end_ms}ms  chunk_id={chunk_id}")
        print(f"      text: {preview}")
        if url:
            print(f"      url:  {url}")
```

Each hit gives you the matching text, the relevance score, a source URL, and either start and end timestamps (for video and audio) or a character range (for documents).

**Spot-check the results.** For each top hit, open the cited source at the cited location and confirm the text really matches. For video, click the `url` and jump to the timestamp. For a document, open the file at the character range. Hallucinated citations are the worst failure mode and catching them here saves work later.

---

## The SDK in two commands

Almost everything in Kurious uses one of these two.

```mermaid
flowchart LR
    A["ingest()<br/>once per file"] --> B[(Project ready)]
    B --> C["search.rag()<br/>any number of times"]
    C --> D[Hits with text,<br/>score, timestamps,<br/>source URL]
```

**Load files.**

```python
client.projects.ingest(project_id, path, wait=True)
```

Pass a folder or a single file. Returns a job object with `job.status` and `job.id`. Run once per file.

**Search.**

```python
client.search.rag(project_id, query="...", limit=5)
```

Returns hits with the matching text, scores, timestamps, and source URLs. Run as often as you want.

| Method | Returns | Use when |
|---|---|---|
| `client.search.rag(...)` | Raw matching chunks with scores, timestamps, and source URLs | You want raw search hits for a custom UI or downstream code. Requires `search_mode="kg_unstructured"`. |
| `client.search.intelligent(...)` | Written answer plus sources | You want a finished answer to show a user. Works on either search mode. |

---

## Troubleshooting

<details>
<summary><b><code>401 Unauthorized</code> on install</b></summary>

Your `AZURE_DEVOPS_TOKEN` is missing or wrong. Re-export it and rerun the install:

```bash
export AZURE_DEVOPS_TOKEN="<your PAT>"
```

If your PAT is being rejected, check that it has the **Packaging (Read)** scope.
</details>

<details>
<summary><b><code>409 Conflict</code> when signing up</b></summary>

The email already has an account. The code in Step 2 handles this automatically: it falls back to `/auth/login`. If you copied it as-is, this should just work.
</details>

<details>
<summary><b>New project, <code>search.rag</code> returns zero hits</b></summary>

Run this once after creating the project:

```python
client.projects.update_config(project_id, search_mode="kg_unstructured")
```

New projects default to `search_mode="unstructured"`. The engine's project-scoped `search.rag` path only runs for `search_mode="kg_unstructured"`. Other modes return zero hits even when your files are correctly indexed. `client.search.intelligent(...)` works either way.
</details>

<details>
<summary><b>Ingest completed but search is empty</b></summary>

Check the index step:

```python
client.projects.get_step_timings(project_id)
```

If `index` shows `count=0`, give it another minute on large files.
</details>

<details>
<summary><b>Video search slow on first query</b></summary>

Cold cache. The first query warms the index. Following queries are sub-second.

A 60-minute video takes about 9 minutes total to fully load before search is ready.
</details>

<details>
<summary><b>Reporting a bug</b></summary>

[Open an issue](https://github.com/Kurious-AI/getting-started/issues/new), pick **Bug report**, include SDK version (`pip show aintropy`), the project ID, the exact call you ran, and the error message.
</details>

---

## Docs

- **API docs:** https://kurious.aintropy.ai/api/docs
- **SDK reference:** coming soon
- **Long-form guide:** see the engine guide

---

## Support

- **Found a bug?** [Open an issue](https://github.com/Kurious-AI/getting-started/issues/new)
- **Question or show-and-tell?** [Discussions](https://github.com/Kurious-AI/getting-started/discussions) or [Discord](https://discord.gg/aintropy-community)
- **Direct help:** know@aintropy.ai

---

## License

Apache 2.0. See [LICENSE](LICENSE).
