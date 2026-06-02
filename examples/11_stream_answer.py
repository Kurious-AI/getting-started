"""
Stream the answer token-by-token instead of waiting for the full response.

Use this for chat UIs where you want output to render as it's generated, or
for long answers where time-to-first-token matters more than total latency.

Run: python examples/11_stream_answer.py
"""

import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])
louisville = next(p for p in client.projects.list().projects if "louisville" in p.name.lower())

for chunk in client.search.intelligent_stream_text(
    project_id=louisville.id,
    query="Summarize the council's housing decisions in 2025.",
    mode="quick",
):
    print(chunk, end="", flush=True)
print()

# Expected output (placeholder — capture actual after Adi ships trial key):
# In 2025 the Louisville council passed three major housing measures: an
# affordable-housing trust fund expansion in March, a short-term rental cap
# in July, and an inclusionary-zoning amendment in October...
