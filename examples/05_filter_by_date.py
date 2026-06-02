"""
Narrow a query to a specific time window.

The SDK doesn't take a structured date-filter parameter — Kurious pulls dates
out of the source files themselves and respects date constraints encoded in
natural language. So just say "in Q1 2026" or "between January and March 2026"
in the question itself.

Run: python examples/05_filter_by_date.py
"""

import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])
louisville = next(p for p in client.projects.list().projects if "louisville" in p.name.lower())

result = client.search.intelligent(
    project_id=louisville.id,
    query="What did the council decide about Bardstown Road zoning between January and March 2026?",
    mode="quick",
)

print(result.answer)
print("\nSources cited (newest first):")
for s in result.sources[:3]:
    print(f"  {s.get('filename', '?')}  ({s.get('date', '?')})")

# Expected output (placeholder — capture actual after Adi ships trial key):
# In Q1 2026, the council deferred the Bardstown variance request twice before
# approving it on March 6 with a 7-2 vote...
# Sources cited (newest first):
#   council_2026-03-06.mp4  (2026-03-06)
#   council_2026-02-13.mp4  (2026-02-13)
