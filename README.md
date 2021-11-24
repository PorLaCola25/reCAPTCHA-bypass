# reCAPTCHA-bypass
Python selenium script to solve reCAPTCHA challenges using speech recognition. As a PoC, google's reCAPTCHA demo page was used, you can test this by running the test.py file.

In order to integrate this with your selenium scripts, simply add the following to your code.

```python
from solve import Solve
...
Solve(driver)
```

Please make sure you are in the daefault content of the page and not inside any iframes .Additionally, make sure that you call set_preference('intl.accept_languages', 'es-ES') in your driver options when initializing it.
