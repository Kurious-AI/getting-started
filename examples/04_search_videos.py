"""
Find the exact moment in a video where a topic was discussed.

Video search returns transcript spans tagged with video_id and timestamp, so you
can jump straight to the clip instead of scrubbing through hours of footage.

Run: python examples/04_search_videos.py
"""

import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])

louisville = next(p for p in client.projects.list().projects if "louisville" in p.name.lower())
hits = client.search.rag(
    project_id=louisville.id,
    query="zoning variance on Bardstown Road",
    limit=5,
)

for h in hits.results[:3]:
    ts = getattr(h, "timestamp_s", None)
    where = f"@{int(ts // 60):02d}:{int(ts % 60):02d}" if ts is not None else ""
    print(f"  {h.filename} {where}  → {h.text[:120]}...")

# Expected output (placeholder — capture actual after Adi ships trial key):
#   council_2025-04-18.mp4 @23:14  → "...the variance on Bardstown Road was approved unanimously..."
#   council_2025-04-11.mp4 @07:02  → "...returning to the Bardstown Road rezoning discussion..."
