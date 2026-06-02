---
name: Bug report
about: Something in the SDK, an example, or the docs didn't work the way the README said it would
title: "[bug] "
labels: bug
assignees: ''
---

## What happened

<!-- One or two sentences. What did you try, and what went wrong? -->

## What you expected

<!-- What did you think would happen, and where in the README/examples is that documented? -->

## How to reproduce

<!-- Minimal code that reproduces the issue. Trim everything that isn't load-bearing. -->

```python
import os
from aintropy import AIntropy

client = AIntropy(api_key=os.environ["KURIOUS_API_KEY"])
# ... your code here
```

## Error / output

<!-- Paste the full traceback or unexpected output here. Redact anything sensitive. -->

```
```

## Environment

- **SDK version:** <!-- `pip show aintropy` → Version -->
- **Python:** <!-- `python --version` -->
- **OS:** <!-- macOS / Linux distro / Windows -->
- **Mode:** <!-- Explore (trial key) or Builder (own key from `kurious init`) -->
- **Project ID:** <!-- if relevant — helps us trace logs -->

## Anything else

<!-- Links to related issues, what you've already tried, screenshots if it's a CLI/UI thing. -->
