<div align="center">

# Kurious

**The search engine your unstructured world was missing.**

Ask any question. Across every format you have: PDFs, videos, tables, scans, transcripts. Get a clear answer with a link back to the exact source. In one call.

[Quickstart](#getting-started) · [Examples](examples/) · [Discord](https://discord.gg/aintropy-community) · [Discussions](https://github.com/Kurious-AI/getting-started/discussions)

</div>

---

## Tagline

The knowledge engine for everything your team already has. From installing the software to your first answer in **60 seconds**. From there to a working search over your own files in under an hour.

---

## Introduction

Most search tools make you do the hard work first.

You sort the files. You convert the formats. You build the pipeline. You hook up the database. You write the code that decides where to look. Somewhere along the way, the actual question you wanted to ask gets lost.

Kurious is built so you can skip all of that.

**One command loads your files.** Point Kurious at a folder. It reads your PDFs, transcribes your audio, pulls frames from your videos, and gets everything ready to search. You do not run any of this yourself.

**One command answers questions.** Ask in plain English. Kurious figures out the best way to find the answer, whether that is searching the text of documents, looking up a number in a spreadsheet, or finding a 30-second moment in an hour-long video.

**Every answer comes with a source.** You always see exactly which file the answer came from, and where in that file. No guessing. No checking by hand.

There are two ways to get started.

| | Mode | Best for | Time to first answer |
|---|---|---|---|
| **Explore** | Use a trial key. Try Kurious on sample data we have already loaded. | "Show me what this thing does." | **About 60 seconds** |
| **Builder** | Run the setup wizard. Load your own files. | "I want to build something with this." | **About 30 minutes** |

We suggest starting with Explore Mode. When you are ready to use your own files, switch to Builder Mode.

---

## Why Kurious

Here is what is usually involved in building this kind of search yourself, and what changes when you use Kurious.

| Without Kurious | With Kurious |
|---|---|
| You pick a database for searching, pick a model to read your files, pick a way to break documents into pieces, then connect them and keep them running. | One software package. A few lines of code. A working answer. |
| You write separate code for searching spreadsheets and searching documents, then decide which to use. | Kurious picks the right approach automatically based on your question. |
| You add separate tools for reading scanned images, transcribing audio, and pulling frames from video. You hope they keep working together. | PDF, Word, MP4, MP3, CSV, and more. All handled in one place. |
| You spend weeks building citations so people can verify the answer. | Every answer comes with a link back to the source. By default. |
| You run servers, monitor them, scale them, and fix them when they break. | We host all of it. You focus on the use case. |

---

## What can you build using Kurious?

These are the kinds of things people are already building with Kurious. If any of these sound like a problem you have, you are in the right place.

**Internal Q&A across thousands of documents.** Drop in your handbook, runbooks, and policy library. Connect Kurious to a Slack bot. People in your company can now ask questions and get answers in seconds.

**Meeting and call intelligence.** Upload your Zoom recordings or sales calls. Ask things like "What did the customer say about renewal in March?" Get back the exact 30-second clip with the timestamp.

**Contract review at scale.** Load 10,000 vendor agreements. Filter by clause, by party, or by signing date, all in natural language. No special legal software needed.

**Research that pulls from many places at once.** Combine quarterly filings (as spreadsheets), analyst PDFs, and earnings call recordings (as MP4 files) in one project. Ask a question and Kurious pulls the answer from all of them together.

**Comparing one question across many sources.** Same question, twenty cities. See where the answers are different. Act on the differences.

If you have content sitting in folders that nobody has time to read through, Kurious is the right tool.

---

## Prerequisites

Before you start, here is everything you need.

- **Python 3.10 or newer** installed on your computer. If you are not sure what version you have, open a terminal and type `python --version` and press enter. If you do not have Python installed, download it from [python.org](https://www.python.org/downloads/).
- **A terminal application.** On a Mac, this is the Terminal app (already installed). On Windows, this is Command Prompt or PowerShell (already installed).
- **About 10 minutes** for Explore Mode, or about 30 minutes for Builder Mode.

That is the full list. You do not need Docker. You do not need to set up any servers. You do not need accounts with any other services.

---

## Getting started

### Step 1. Explore Mode (about 60 seconds, no signup)

You will get a trial key that lets you search five sample collections we have already prepared for you:

1. Louisville city council meetings (video)
2. Seattle city council meetings (video)
3. New Jersey Open Data (spreadsheets)
4. A legal video archive
5. A chemistry research dataset

This is the fastest way to see what Kurious can do.

**1. Install the Kurious software**

Open your terminal. Run these two commands, one at a time. Wait for the first to finish before running the second.

```bash
pip install artifacts-keyring
```

```bash
pip install "aintropy>=0.5.5,<0.6" --index-url "https://pkgs.dev.azure.com/AIntropy-DevOps/Kurious-SDK/_packaging/kurious-sdk-pypi/pypi/simple/"
```

The first command installs a small helper that handles your login automatically. The second command installs Kurious.

If you see an error that says `401 Unauthorized`, do not worry. Skip down to the [Troubleshooting](#troubleshooting) section for a fix, then come back.

**2. Set your trial key**

Once you have your trial key (we will send it to you), put it into your terminal like this. Replace the placeholder text with the real key.

```bash
export KURIOUS_API_KEY="trial_REPLACE_ME"
```

This tells Kurious who you are. You only need to do this once per terminal session.

**3. Ask your first question**

Save the code below into a file called `first_query.py`. Then in your terminal, run:

```bash
python first_query.py
```

Here is the code:

```python
import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])

louisville = next(
    p for p in client.projects.list().projects
    if "louisville" in p.name.lower()
)

result = client.search.intelligent(
    project_id=louisville.id,
    query="What did the council decide about affordable housing?",
    mode="quick",
)

print(result.answer)
for s in result.sources[:3]:
    print(f"  {s.get('filename', '?')} (score={s.get('score', 0):.2f})")
```

You just searched hundreds of hours of city council video and got an answer back, with sources. That is the whole loop.

When you are ready for more, open the [`examples/`](examples/) folder. There are ten more short scripts in there. Find a moment in a video by topic. Filter by date. Search across documents and video at the same time. Compare two cities side by side. Each script is about 15 lines and runs against the same trial key.

### Step 2. Builder Mode (your own data, about 30 minutes)

When you are ready to load your own files, run the setup wizard.

```bash
kurious init
```

The wizard will ask you a few questions:

- Your full name
- Your work email
- Your organization name
- A name for your project (something short and clear like `q3-contracts`, `support-tickets`, or `2025-handbook`)

When it finishes, your API key is saved to your computer and ready to use. There is no browser step. There is no copy-and-paste.

Then load your files. Save this code to a file and run it.

```python
import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])
project_id = client.projects.list().projects[0].id

job = client.projects.ingest(project_id, "./my-docs/", wait=True)
print(f"Loading is {job.status}")

result = client.search.intelligent(
    project_id=project_id,
    query="Your question here"
)
print(result.answer)
```

A few things worth knowing:

- You can pass a single file instead of a folder. For example, `"./meeting.mp4"` will load just that video. Kurious will transcribe the audio, pull out frames, and prepare everything in one step.
- A 60-minute video takes about 10 to 15 minutes to finish loading.
- If you want to watch the progress, add `on_progress=lambda j: print(j.status)` to the call.

**File types Kurious supports out of the box:**

PDF, Word documents (`.docx`), Markdown (`.md`), plain text (`.txt`), images (`.png`, `.jpg`), audio (`.mp3`, `.wav`), video (`.mp4`), spreadsheets (`.csv`), and Parquet data files.

Kurious looks at each file, figures out what type it is, and handles it automatically. You do not have to label anything.

---

## The two commands you will use most

Almost everything in Kurious comes down to two commands. Once you understand these, you understand the product.

**1. Load your files into a project**

```python
client.projects.ingest(project_id, path)
```

Pass it a folder or a single file. Kurious will:

- Upload everything
- Read each file and break it into pieces that are easy to search
- For audio and video, transcribe the speech and pull out frames
- Store it all so you can search it instantly

You only run this once per file. After that, the file is ready forever.

**2. Ask a question**

```python
client.search.intelligent(project_id=..., query="...")
```

Pass it a question in plain English. Kurious will return an answer and the sources behind it. Behind the scenes, Kurious is choosing the best way to search based on your question, whether that is looking through documents, pulling numbers from a spreadsheet, or finding moments in a video. You do not have to decide.

That is the loop. Load files once. Ask questions as often as you want.

---

## SDK reference and full docs

| | |
|---|---|
| **API documentation (Swagger)** | https://kurious.aintropy.ai/api/docs |
| **SDK reference site** | Coming soon with the next release |
| **Long-form guide** | Loading your own data, advanced search, video processing, going to production |

---

## Examples

Twelve ready-to-run scripts in the [`examples/`](examples/) folder. Each one shows a single capability against the sample data. Each is around 10 to 15 lines, with comments to walk you through it.

| # | Script | What it shows |
|---|---|---|
| 01 | `01_hello_search.py` | Your first query: Louisville council on housing |
| 02 | `02_list_projects.py` | Every sample project you can search |
| 03 | `03_get_project_info.py` | What is inside a project: file counts, formats, coverage |
| 04 | `04_search_videos.py` | Find the exact 30-second clip on a topic |
| 05 | `05_filter_by_date.py` | Same query, narrowed to a date range |
| 06 | `06_find_a_person.py` | Every mention of a speaker across hours of video |
| 07 | `07_cross_modal.py` | One query, evidence from video and PDF together |
| 08 | `08_quick_vs_deep_think.py` | Fast answers vs. more thorough answers |
| 09 | `09_compare_projects.py` | Same question, two projects, side by side |
| 10 | `10_show_citations.py` | Every source span behind an answer |
| 11 | `11_stream_answer.py` | Stream the answer one word at a time |
| 12 | `12_see_routing_decision.py` | See which approach Kurious chose to answer |

To run any of them:

```bash
python examples/01_hello_search.py
```

---

## Troubleshooting

<details>
<summary><b>I get <code>401 Unauthorized</code> when installing.</b></summary>

The login helper could not authenticate you automatically. Here is how to fix it:

1. Go to [dev.azure.com/AIntropy-DevOps](https://dev.azure.com/AIntropy-DevOps).
2. Click your avatar in the top right.
3. Click **Personal access tokens**.
4. Create a new token with the scope set to **Packaging (Read)**.
5. Copy the token.
6. In your terminal, run:

   ```bash
   export AZURE_DEVOPS_EXT_PAT="<your-token-here>"
   ```

7. Run the install command again.
</details>

<details>
<summary><b>I get <code>403 Forbidden</code> when searching a project.</b></summary>

Your API key does not have permission for that project. Trial keys work on all sample projects. Keys you create with `kurious init` only work on the project you created them with.
</details>

<details>
<summary><b>I created a new project and search returns nothing.</b></summary>

New projects start with one of the search modes turned off. Run this one time after you create the project:

```python
client.projects.update_config(project_id, search_mode="kg_unstructured")
```

This only matters for one specific search function. The main `client.search.intelligent(...)` works either way.
</details>

<details>
<summary><b>Loading finished but search returns nothing.</b></summary>

The system might still be writing your data to the search index. Run this to check:

```python
client.projects.get_step_timings(project_id)
```

If the `index` step shows `count=0`, give it another minute on large collections, then try again.
</details>

<details>
<summary><b>Video search is slow the first time.</b></summary>

That is expected. The system warms up on the first query. After that, queries are very fast. A 60-minute video takes about 10 to 15 minutes to fully prepare before any search will be fast.
</details>

<details>
<summary><b>Where do I report a bug?</b></summary>

[Open an issue here](https://github.com/Kurious-AI/getting-started/issues/new) and pick **Bug report**. Please include:

- Your SDK version (run `pip show aintropy` to find it)
- Your project ID
- The exact code you ran
- The error message you saw
</details>

---

## Roadmap

New features will be listed here as they ship.

---

## Support

| | |
|---|---|
| **Found a bug?** | [Open an issue](https://github.com/Kurious-AI/getting-started/issues/new) |
| **Got a question, or want to share what you built?** | [GitHub Discussions](https://github.com/Kurious-AI/getting-started/discussions) or [join our Discord](https://discord.gg/aintropy-community) |
| **Need direct help?** | know@aintropy.ai |

---

## License

Apache 2.0. See [LICENSE](LICENSE). Use it, fork it, build a company on it. We only ask that you keep the attribution.
