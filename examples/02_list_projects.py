"""
See every demo project you have access to.

Think of this as `ls` for Kurious — useful for picking a project_id before any
of the other examples. The trial key has read access to ~5 demo projects.

Run: python examples/02_list_projects.py
"""

import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])

projects = client.projects.list().projects
print(f"{len(projects)} project(s) available:\n")
for p in projects:
    print(f"  {p.id}  {p.name}")

# Expected output (placeholder — capture actual after Adi ships trial key):
# 5 project(s) available:
#   <uuid>  louisville-legal-video
#   <uuid>  seattle-council
#   <uuid>  nj-open-data
#   <uuid>  legal-video-archive
#   <uuid>  chemrag
