"""
Narrow a query to a specific date range.

Same question as example 04, but limited to Q1 2026 — useful when you want
"what did they say last quarter" rather than "what did they ever say."

Run: python examples/05_filter_by_date.py
"""

import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])

louisville = next(p for p in client.projects.list().projects if "louisville" in p.name.lower())

# TODO(adi): confirm the date-filter kwarg shape in the SDK — using filters={...} as the placeholder
hits = client.search.rag(
    project_id=louisville.id,
    query="zoning variance on Bardstown Road",
    limit=5,
    filters={"date_from": "2026-01-01", "date_to": "2026-03-31"},
)

for h in hits.results[:3]:
    print(f"  {h.filename} ({getattr(h, 'date', '?')})  → {h.text[:100]}...")

# Expected output (placeholder — capture actual after Adi ships trial key):
#   council_2026-02-13.mp4 (2026-02-13)  → "...the Bardstown variance request was deferred..."
#   council_2026-03-06.mp4 (2026-03-06)  → "...council voted to approve the variance..."
