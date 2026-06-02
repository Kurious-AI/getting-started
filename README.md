<div align="center">

# Kurious

**A step-by-step tutorial: from installing the SDK to running your first search on your own files.**

[Quickstart](#getting-started) · [Discord](https://discord.gg/aintropy-community) · [Discussions](https://github.com/Kurious-AI/getting-started/discussions)

</div>

---

## Prerequisites

Before you start, you need these four things.

| | You need | How to check or get it |
|---|---|---|
| 1 | **Python 3.12 or newer** | Open your terminal and run `python --version`. If you do not have it, download from [python.org](https://www.python.org/downloads/). |
| 2 | **A terminal app** | Mac: Terminal. Windows: PowerShell. Both come pre-installed. |
| 3 | **Your Aintropy access token (PAT)** | Aintropy emails you a Personal Access Token. This is what unlocks the SDK download. |
| 4 | **A file to search** | Any PDF, Word doc, spreadsheet, image, audio, or video file on your computer. For video: `mp4`, `mov`, `mkv`, or `webm`. |

> [!NOTE]
> No Docker. No servers. No other accounts. The SDK installs through `pip` like any other Python package.

---

## Install the SDK

Four commands in your terminal. Run them one at a time, waiting for each to finish before the next.

**1. Set your access token**

Replace the placeholder with the token Aintropy sent you, then run:

```bash
export AZURE_DEVOPS_TOKEN="<paste your PAT here>"
```

**2. Install Kurious**

```bash
pip install --upgrade "aintropy==0.5.5" \
  --index-url "https://aintropy:${AZURE_DEVOPS_TOKEN}@pkgs.dev.azure.com/AIntropy-DevOps/Kurious-SDK/_packaging/kurious-sdk-pypi/pypi/simple/" \
  --extra-index-url "https://pypi.org/simple/"
```

**3. Install two helpers used later in the tutorial**

```bash
pip install jupyter requests
```

**4. Verify everything worked**

```bash
python -c "import aintropy; print(aintropy.__version__)"
```

You should see `0.5.5` printed. If you do, you are ready for the next section.

---

## Getting started

Five steps from zero to a working search.

```mermaid
flowchart LR
    A[Step 1<br/>Pick a file] --> B[Step 2<br/>Sign in +<br/>get API key] --> C[Step 3<br/>Create<br/>a project] --> D[Step 4<br/>Load<br/>your file] --> E[Step 5<br/>Search]
```

---

### Step 1 of 5. Point at your file

Tell Python where your file lives. Replace the path with your own.

```python
import os

FILE_PATH    = os.path.expanduser("~/Desktop/my_video.mp4")   # replace
PROJECT_NAME = "my-first-project"                              # replace

assert os.path.isfile(FILE_PATH), f"FILE_PATH does not exist: {FILE_PATH}"
size_mb = os.path.getsize(FILE_PATH) / (1024 * 1024)
print(f"  file: {FILE_PATH}")
print(f"  size: {size_mb:.1f} MB")
```

**What this does:** points Python at your file, confirms it actually exists, and prints its size. If you get an `AssertionError`, the path is wrong, fix it and rerun.

---

### Step 2 of 5. Sign in and get an API key

Kurious uses three small steps to set up your session:

1. **Sign up** for an account (or log in if you already have one). This gets you a temporary login token called a JWT.
2. **Exchange the JWT** for a long-lived API key.
3. **Build the SDK client** using the API key.

Replace the four placeholders (email, password, name, company) with your own values.

<details>
<summary><b>Click to expand: full sign-in code (copy and replace the four placeholders)</b></summary>

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

</details>

**What this does:** signs you in, gets your API key, and builds a `client` object you'll use for everything else. Run this once per session.

**The fields you can set when creating an API key:**

| Field | What it means |
|---|---|
| `name` | A label for this key. Anything you want. |
| `access_type` | `read_write` lets you upload files. `read_only` only allows searching. |
| `max_index` | How many projects this key can access. |
| `max_size_gb` | Total storage this key can use. |
| `expiry_days` | How long the key stays valid. |

---

### Step 3 of 5. Create your project

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

**What this does:** asks Kurious if a project with your chosen name already exists. If yes, reuses it. If no, creates it. Then saves the project ID for the next steps.

> [!IMPORTANT]
> **Run this one extra line right after creating a new project:**
> ```python
> client.projects.update_config(PROJECT_ID, search_mode="kg_unstructured")
> ```
> Without it, `client.search.rag(...)` returns zero results even when your files are loaded correctly. Most common gotcha in the tutorial. `client.search.intelligent(...)` is not affected.

---

### Step 4 of 5. Load your file into the project

One call uploads your file and gets it ready to search.

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

**What this does:** uploads your file, parses it, transcribes any audio or video, analyzes any video frames, and indexes everything. The `on_progress` callback prints a live status update so you know it is still working.

**How long it takes:**

| Content type | Roughly |
|---|---|
| Documents (PDF, DOCX, CSV, etc.) | Seconds |
| Audio | 1 to 2 minutes per hour of audio |
| Video | About 9 minutes per hour of video |

You only run this once per file.

---

### Step 5 of 5. Run your first search

<details>
<summary><b>Click to expand: full search code with formatted output</b></summary>

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

</details>

**What this does:** runs your queries against the project. For each query, prints the top 3 hits: the matching text, the relevance score, the source URL, and either timestamps (for video and audio) or character ranges (for documents).

> [!IMPORTANT]
> **Always spot-check your first results.** Click the source URL and confirm the text really matches what is at the cited location. Hallucinated citations are the worst failure mode and catching them now saves work later.

---

## The SDK in two commands

After setup, almost everything you do uses one of these two.

```mermaid
flowchart LR
    A["ingest()<br/>once per file"] --> B[(Project ready)]
    B --> C["search()<br/>any number of times"]
    C --> D[Hits with text,<br/>score, timestamps,<br/>source URL]
```

**Load files:**

```python
client.projects.ingest(project_id, path, wait=True)
```

Pass a folder or a single file. Returns a job object with `job.status` and `job.id`. Run once per file.

**Search:**

| Method | Returns | Use when |
|---|---|---|
| `client.search.rag(...)` | Raw matching chunks with scores, timestamps, and source URLs | You want raw hits for a custom UI or downstream code. Requires `search_mode="kg_unstructured"`. |
| `client.search.intelligent(...)` | Written answer plus sources | You want a finished answer to show a user. Works on either search mode. |

---

## Tips & gotchas

Things worth knowing before you hit them.

> [!WARNING]
> **`401 Unauthorized` during install.** Your `AZURE_DEVOPS_TOKEN` is missing or wrong. Re-export it and rerun the install command. If your token is still rejected, check that it has the **Packaging (Read)** scope.

> [!NOTE]
> **`409 Conflict` during signup is expected.** It just means the email already has an account. The Step 2 code handles this automatically by falling back to login. Nothing to fix.

> [!IMPORTANT]
> **Always run `update_config` on a fresh project.** New projects default to `search_mode="unstructured"`, with which `client.search.rag(...)` silently returns zero hits. The one-line fix:
> ```python
> client.projects.update_config(project_id, search_mode="kg_unstructured")
> ```
> This is the single most common gotcha. `client.search.intelligent(...)` is not affected.

> [!TIP]
> **Search hit field names vary by file type.** A hit's score may live at `_score`, `score`, or `relevance_score`. Text may be at `text`, `content`, or `excerpt`. URLs at `video_url`, `source_url`, `url`, or `document_url`. Always use `.get()` with fallbacks, like the Step 5 code does, so your script works across file types.

> [!NOTE]
> **First video query is slow, the rest are fast.** The first query warms the index. Following queries are sub-second. A 60-minute video also takes about 9 minutes to fully load before any search is ready.

> [!TIP]
> **"Ingest completed" but search returns empty?** The index might still be propagating. Check it with:
> ```python
> client.projects.get_step_timings(project_id)
> ```
> If `index` shows `count=0`, give it another minute and try again.

> [!TIP]
> **Kurious does not scrape or convert.** Make sure your file is already in a supported format (`pdf`, `docx`, `txt`, `md`, `csv`, `parquet`, `png`, `jpg`, `mp3`, `wav`, `mp4`, `mov`, `mkv`, `webm`) before ingesting.

> [!TIP]
> **Search runs inside one project at a time.** To search across multiple corpora, either use one project per corpus and query each separately, or load everything into one project and filter at query time.

> [!TIP]
> **Bulk-ingesting many files?** Use `wait=False` in `ingest()` and a Python loop to fan jobs out, then poll for completion. Concurrent ingests share GPU capacity on the backend, so even parallel calls will run partly serially. Plan capacity accordingly.

> [!TIP]
> **Set API key quotas to fit your corpus.** When you create an API key, `max_index` is the number of projects this key can access and `max_size_gb` is the total storage. Plan for the size of your corpus.

> [!NOTE]
> **Reporting a bug.** [Open an issue](https://github.com/Kurious-AI/getting-started/issues/new), pick **Bug report**, and include your SDK version (`pip show aintropy`), the project ID, the exact call you ran, and the error message.

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
