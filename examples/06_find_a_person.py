"""
Find every mention of a specific speaker across a video archive.

Phrase the person's name directly in the query — Kurious picks up speaker
attributions from the transcript and returns all clips that match. Works for
named entities too (mayor, council president, specific witnesses).

Run: python examples/06_find_a_person.py
"""

import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])
louisville = next(p for p in client.projects.list().projects if "louisville" in p.name.lower())

result = client.search.intelligent(
    project_id=louisville.id,
    query='Find every time Councilmember Arthur spoke about public transit. Quote the relevant lines.',
    mode="quick",
)

print(result.answer[:500])
print(f"\n{len(result.sources)} clips referenced:")
for s in result.sources[:5]:
    print(f"  {s.get('filename', '?')}")

# Expected output (placeholder — capture actual after Adi ships trial key):
# Councilmember Arthur addressed transit in three separate sessions...
# 5 clips referenced:
#   council_2025-09-12.mp4
#   council_2025-11-07.mp4
#   ...
