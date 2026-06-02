"""
One query, evidence from multiple file types in the same project.

Cross-modal retrieval blends video transcripts and document text in a single
answer when the project contains both. Useful when the question needs context
from one modality (the recorded debate) and ground-truth from another
(the formal agenda PDF or budget document).

Run: python examples/07_cross_modal.py
"""

import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])
louisville = next(p for p in client.projects.list().projects if "louisville" in p.name.lower())

result = client.search.intelligent(
    project_id=louisville.id,
    query="What did the agenda list under transportation, and what did the council actually say during the discussion?",
    mode="quick",
)

print(result.answer)
filetypes = {s.get("filename", "").rsplit(".", 1)[-1] for s in result.sources}
print(f"\nGrounded across {len(filetypes)} file types: {sorted(filetypes)}")

# Expected output (placeholder — capture actual after Adi ships trial key):
# The transportation block of the agenda listed three items: ...
# During the live discussion, councilmembers raised concerns about ...
# Grounded across 2 file types: ['mp4', 'pdf']
