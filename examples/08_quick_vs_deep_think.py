"""
Same query, two retrieval modes — speed vs depth.

`quick` returns in a couple of seconds with single-pass retrieval. `deep` runs an
agent loop that decomposes the question, retrieves multiple times, and reasons over
intermediate results — slower, but better for multi-hop questions.

Run: python examples/08_quick_vs_deep_think.py
"""

import os, time
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])
louisville = next(p for p in client.projects.list().projects if "louisville" in p.name.lower())
query = "Compare how the council handled the 2024 and 2025 stormwater budgets."

# TODO(adi): confirm the deep mode name — could be "deep", "agentic", "deep_think"
for mode in ("quick", "deep"):
    t0 = time.perf_counter()
    r = client.search.intelligent(project_id=louisville.id, query=query, mode=mode)
    print(f"[{mode:5s}  {(time.perf_counter() - t0):>5.1f}s]  {r.answer[:200]}...\n")

# Expected output (placeholder — capture actual after Adi ships trial key):
# [quick    2.3s]  The 2024 budget allocated $X for stormwater; 2025 increased it to $Y...
# [deep    18.7s]  Across both years, the council shifted from a single-line-item allocation
#                  toward a tiered structure. In 2024 the discussion focused on...
