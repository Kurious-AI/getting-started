# Kurious

> The AI knowledge engine for digital and physical AI. Video, sensors, documents - cited answers in under a second.

Kurious is the AI knowledge engine that handles the messy work of multi-modal retrieval so you do not have to. Point the Python SDK at your data - video, sensor streams, document corpora, structured tables - and ask any question in natural language. You get back answers grounded in your source material, with every claim cited to the exact moment, page, or row it came from.

This repo is your starting point. Run a query against our demo data in two minutes (Explore Mode), or wire Kurious into your own data with one command (Builder Mode).

---

## Why Kurious

- **One semantic layer over every modality.** Video, sensors, documents, structured tables - ingested through one Python SDK. No stitching Whisper to LangChain to Pinecone to your own glue code.

- **Cited answers, not vibes.** Every response points back to the exact source moment, page, or row in your data. If Kurious cannot find supporting evidence, it says so rather than fabricating.

- **Fast and cheap, not "fast or cheap".** Designed for sub-second query latency at production cost. We publish accuracy, latency, and cost numbers on our public benchmark dashboard - no hidden trade-offs.

- **Cross-modal retrieval out of the box.** Ask a text question against a video. Ask a sensor question against a paper. The retrieval layer is multi-sensory by design, not bolted on top of single-modal RAG.

- **Built for Physical AI as a first-class citizen.** Sensor streams, robot logs, and world-model data are not afterthoughts. They are core to how we built ingestion and retrieval - the same engine powers Digital and Physical AI use cases.

---

## What can you build using Kurious

Kurious can do four things:

- **Natural-language search across all your data.** Ask a question in plain English against your video, sensor, document, and structured data. Kurious finds the relevant moments regardless of where they live.

- **Cited, evidence-grounded answers.** Every response points to the exact source moment, page, or row. When the evidence is not there, Kurious says so rather than fabricating.

- **Cross-modal retrieval.** Ask a text question against video. Ask a sensor question against documents. The retrieval layer does not care about the source modality.

- **Real-time at production scale.** Sub-second query latency at production cost. Suitable for live agents, dashboards, and customer-facing tools.

**Beta solutions built on Kurious:**

| Beta | Domain | Try it |
|---|---|---|
| **NJ Open Data** | Public records, NJ municipal data | [Live demo →](https://huggingface.co/spaces/aintropy-ai/nj-open-data-leaderboard-v1) |
| **Legal Videos** | Legal depositions, video evidence | [Live demo →](https://huggingface.co/spaces/aintropy-ai/legal-videos-leaderboard-v1) |
| **chemRAG** | Chemistry papers, lab notes | [Live demo →](https://huggingface.co/spaces/aintropy-ai/chemRAG-leaderboard-v1) |
| **Skyfire** | Drone footage and telemetry intelligence | Upcoming beta |
| **Louisville** | *(in development)* | Upcoming beta |
| **Enquire** | *(in development)* | Upcoming beta |
| **Zivo** | *(in development)* | Upcoming beta |

Watch this space - the upcoming betas will be linked here as they launch.

See `examples/` in this repo for runnable end-to-end code for each.

---

## Prerequisites

- Python 3.9 or newer
- A package manager: `pip`, `uv`, or `poetry`
- Internet access (queries hit the hosted Kurious trial cluster)
- For Builder Mode only: an email address (used during signup, you keep ownership of your key)

---

## Getting started

Two paths. Pick based on what you want to do today.

### Step 1: Explore Mode — no signup, ~2 minutes

Use the shared trial API key to query our demo projects. Read-only access to public demo data (NJ Open Data, Legal Videos, chemRAG). Fastest way to feel the SDK without committing.

```bash
pip install kurious
```

```python
import kurious

# The shared trial key lives in .env.example in this repo
client = kurious.Client(api_key="<trial-key-from-readme>")

result = client.query(
    "What citation evidence supports the contract clause interpretation in this collection?",
    project="legal-videos-demo",
)

print(result.answer)
for citation in result.citations:
    print(f"  - {citation.source} @ {citation.location}")
```

What you get back: an answer string plus a list of citations - each one pointing to a video moment, document page, or data row in the demo project.

### Step 2: Builder Mode — signup, your own data, ~5 minutes

Spin up your own project, ingest your own data, get your own API key.

```bash
kurious init
```

The interactive wizard asks for your name, email, organization, and project name. It returns an API key, writes it to your local config, and prints your project ID.

```python
import kurious

client = kurious.Client.from_config()   # reads the key written by `kurious init`

# Ingest a folder of mixed-modality data (video, docs, structured, sensor)
client.ingest("/path/to/my/data")

# Query against your project
result = client.query("Your real question against your real data")
print(result.answer)
```

That is the full Builder Mode loop. Ingest, query, iterate.

---

## SDK reference and full docs

Full SDK docs: **`docs.kurious.aintropy.ai`** *(coming soon - placeholder)*

In the meantime:

- `kurious.help()` prints inline SDK help in the REPL
- `examples/` in this repo has runnable end-to-end code for every Kurious capability
- Type hints are complete on every public method - your IDE will autocomplete

---

## Troubleshooting and FAQ

**My query returns no citations.**
Either the question is too broad, or the project does not contain relevant data. Try narrowing the question to the modality you expect (for example: *"in the video footage, when did..."*).

**`kurious init` hangs at the email step.**
Email verification is sent via a one-time link. Check your inbox and spam. If nothing arrives in five minutes, file a bug (see below).

**My ingest is slower than I expected.**
Video is the slowest modality and scales with total duration. Roughly one minute of ingest per ten minutes of video on the trial cluster. Builder Mode customers can request faster ingest on a paid tier.

**The trial API key is rate-limited.**
Yes, intentionally. Explore Mode is for evaluation, not production. If you hit the limit, run `kurious init` to switch to Builder Mode with your own key and higher limits.

**Something is broken or unexpected. How do I report it?**
Open a new issue using the **Bug report** template in this repo. It auto-prompts for SDK version, modality, the call you made, and what you saw vs expected. We aim to triage and tag every bug within one business day.

---

## Roadmap

*Yet to be updated.*

---

## Support channels

*Yet to be updated.*

---

## License

Apache 2.0 - see [LICENSE](./LICENSE).
