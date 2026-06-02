"""
After an answer, list every source chunk that grounded it.

Demonstrates Kurious's citation transparency — every answer carries the exact
source spans (file + char range or timestamp) it pulled from. Useful when you
need to verify or quote the underlying evidence.

Run: python examples/10_show_citations.py
"""

import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])
louisville = next(p for p in client.projects.list().projects if "louisville" in p.name.lower())

r = client.search.intelligent(
    project_id=louisville.id,
    query="What was the council's vote on the 2025 transit budget?",
    mode="quick",
)
print(r.answer, "\n")

for i, s in enumerate(r.sources, 1):
    span = (
        f"chars {s['char_start']}-{s['char_end']}" if "char_start" in s
        else f"@{s.get('timestamp_s', '?')}s"
    )
    print(f"  [{i}] {s.get('filename', '?')}  {span}  (score={s.get('score', 0):.2f})")
    print(f"      \"{s.get('text', '')[:140]}...\"")

# Expected output (placeholder — capture actual after Adi ships trial key):
# The 2025 transit budget passed 7-2 on March 14, 2025...
#
#   [1] council_2025-03-14.mp4  @1942s  (score=0.91)
#       "...the motion to approve the transit budget at $42M passes seven to two..."
#   [2] budget_summary_2025.pdf  chars 4120-4280  (score=0.83)
#       "...transit allocation: $42,000,000 (up from $38M in 2024)..."
