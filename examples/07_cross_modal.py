"""
One query, both video content and structured records.

Cross-modal search asks a question that needs evidence from two file types at once
— here, a council vote (video transcript) cross-referenced with a budget table
(structured CSV). Kurious routes the relevant slice of the query to each pipeline.

Run: python examples/07_cross_modal.py
"""

import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])

# nj-open-data has structured budget tables; louisville has council video.
# For cross-modal in a single project, both modalities live in the same project_id.
nj = next(p for p in client.projects.list().projects if "nj" in p.name.lower())

result = client.search.intelligent(
    project_id=nj.id,
    query="Which agencies received budget increases over 10% in 2025, and what was discussed about them in the committee hearings?",
    mode="quick",
)

print(result.answer)
print(f"\nUsed {len(result.sources)} sources across {len({s.filename.rsplit('.', 1)[-1] for s in result.sources})} file types")

# Expected output (placeholder — capture actual after Adi ships trial key):
# Three agencies received >10% increases in FY2025: ...
# Used 7 sources across 2 file types
