"""
Find the exact moment in a video where a topic was discussed.

Video segments are indexed as transcript spans with timestamps, so retrieval
returns the exact 30-second clip — jump straight to it instead of scrubbing
through hours of footage.

Run: python examples/04_search_videos.py
"""

import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])

louisville = next(p for p in client.projects.list().projects if "louisville" in p.name.lower())
res = client.search.rag(
    project_id=louisville.id,
    query="zoning variance on Bardstown Road",
    limit=5,
)

for hit in res.hits[:3]:
    ts = hit.get("timestamp_s")
    where = f"@{int(ts // 60):02d}:{int(ts % 60):02d}" if ts is not None else ""
    print(f"  {hit.get('filename', '?')} {where}  → {hit.get('text', '')[:120]}...")

# Expected output (placeholder — capture actual after Adi ships trial key):
#   council_2025-04-18.mp4 @23:14  → "...the variance on Bardstown Road was approved unanimously..."
#   council_2025-04-11.mp4 @07:02  → "...returning to the Bardstown Road rezoning discussion..."
