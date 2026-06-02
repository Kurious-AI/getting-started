"""
Your first Kurious query.

Asks "What did the council decide about affordable housing?" against the Louisville
city-council demo project. Returns a grounded answer plus the source recordings
the answer was drawn from. Confirms your setup works end-to-end.

Run: python examples/01_hello_search.py
"""

import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])

louisville = next(p for p in client.projects.list().projects if "louisville" in p.name.lower())
result = client.search.intelligent(
    project_id=louisville.id,
    query="What did the council decide about affordable housing?",
    mode="quick",
)

print(result.answer)
print("\nSources:")
for s in result.sources[:3]:
    print(f"  {s.filename} (score={s.score:.2f})")

# Expected output (placeholder — capture actual after Adi ships trial key):
# The council passed Ordinance 2025-... allocating $X million toward affordable housing...
# Sources:
#   council_meeting_2025-03-14.mp4 (score=0.87)
#   council_meeting_2025-03-21.mp4 (score=0.81)
#   ...
