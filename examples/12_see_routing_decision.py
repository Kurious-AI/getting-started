"""
See which retrieval pipeline Kurious picked for your query.

`intelligent` routes each query to one of three pipelines under the hood:
unstructured (RAG over documents/video), structured (NL2SQL over tables), or
knowledge-graph. The `routing_decision` field on the result shows which one
ran — useful for debugging when an answer looks off.

Run: python examples/12_see_routing_decision.py
"""

import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])
louisville = next(p for p in client.projects.list().projects if "louisville" in p.name.lower())

for query in (
    "What did the mayor say about housing in October?",                     # likely unstructured
    "How many votes did the 2025 transit budget receive?",                  # may route to structured
    "Which councilmembers were on the transportation committee in 2024?",   # may route to KG
):
    r = client.search.intelligent(project_id=louisville.id, query=query, mode="quick")
    print(f"[{r.routing_decision:14s}]  {query}")
    print(f"                  → {r.answer[:140]}...\n")

# Expected output (placeholder — capture actual after Adi ships trial key):
# [unstructured  ]  What did the mayor say about housing in October?
#                   → In October the mayor called for...
# [structured    ]  How many votes did the 2025 transit budget receive?
#                   → 7 to 2 in favor (March 14, 2025)
# [kg            ]  Which councilmembers were on the transportation committee in 2024?
#                   → Arthur, James, and Whitehall served on the transportation committee...
