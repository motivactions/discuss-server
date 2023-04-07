# Discuss Module

This module handle discussion about related object.

```python
from server import hooks


@hooks.register("API_V1_URL_PATTERNS")
def register_discuss_urls():
    return "discuss/", "discuss.api.v1.urls"
```
