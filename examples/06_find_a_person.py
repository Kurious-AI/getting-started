"""
Find every mention of a specific speaker across a video archive.

Useful for "what has councilmember X said about Y?" — speaker recognition pulls
back all clips where that voice (or named entity) appears.

Run: python examples/06_find_a_person.py
"""

import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])

louisville = next(p for p in client.projects.list().projects if "louisville" in p.name.lower())

# TODO(adi): confirm whether speaker filter is a separate method or a query operator
result = client.search.intelligent(
    project_id=louisville.id,
    query='Find every clip where Councilmember Arthur speaks about transit',
    mode="quick",
)

print(result.answer[:500])
print(f"\n{len(result.sources)} clips referenced:")
for s in result.sources[:5]:
    print(f"  {s.filename}")

# Expected output (placeholder — capture actual after Adi ships trial key):
# Councilmember Arthur addressed transit funding in three separate sessions...
# 5 clips referenced:
#   council_2025-09-12.mp4
#   council_2025-11-07.mp4
#   ...
