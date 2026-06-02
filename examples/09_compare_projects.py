"""
Run the same question against two corpora, side by side.

Useful for "how does city A handle X vs city B?" — same query, two project_ids,
compare the answers directly.

Run: python examples/09_compare_projects.py
"""

import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])

projects = client.projects.list().projects
louisville = next(p for p in projects if "louisville" in p.name.lower())
seattle = next(p for p in projects if "seattle" in p.name.lower())

query = "How does the council approve a new zoning variance? What's the process?"

for p in (louisville, seattle):
    r = client.search.intelligent(project_id=p.id, query=query, mode="quick")
    print(f"--- {p.name} ---")
    print(r.answer[:300])
    print()

# Expected output (placeholder — capture actual after Adi ships trial key):
# --- louisville-legal-video ---
# In Louisville, zoning variances are heard first by the Board of Zoning Adjustment...
#
# --- seattle-council ---
# Seattle handles variances through the Department of Construction and Inspections...
