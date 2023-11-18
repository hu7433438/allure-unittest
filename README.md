# allure-unittest

unittest Allure integration

```python
import unittest
from allure_unittest import Run

suit = unittest.defaultTestLoader.loadTestsFromTestCase(unittest.TestCase)
Run('allure_report_source_path', suit, clean=True)
```
