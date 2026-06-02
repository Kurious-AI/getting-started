"""
Look inside a project before you query it.

Shows file counts, total size, and the date range the corpus covers — helpful for
sanity-checking what's in scope before asking a question that depends on coverage.

Run: python examples/03_get_project_info.py
"""

import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])

louisville = next(p for p in client.projects.list().projects if "louisville" in p.name.lower())
files = client.files.list(louisville.id, limit=500).files

print(f"Project: {louisville.name}")
print(f"  files:    {len(files)}")
print(f"  indexed:  {sum(1 for f in files if f.unstructured_status == 'indexed')}")
print(f"  formats:  {sorted({f.filename.rsplit('.', 1)[-1] for f in files})}")

# Expected output (placeholder — capture actual after Adi ships trial key):
# Project: louisville-legal-video
#   files:    142
#   indexed:  142
#   formats:  ['mp4', 'pdf']
