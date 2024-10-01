- Most of the doc strings are redundant.
    - As a rule of thumb: you write a doc string if the function and parameter names can't provide all the information. But usually, they can.
    - And some of your docstring are realllllly long. this means the code is not self explanatory. and that's bad.
- You have a bug - I can provide a CORRECT letter that was already provided, again again, and gain more and more points.
- If your code can work with a list of words, provide a sample file so we can see the format



A word about comments and docstrings: code is a leaving things that developers keep updating and upgrading. And they forget to update the docstring and documentation, and slowly but surly those docs becomes archiological artifacts of the past funcionality of the code.

Documentation is important for external APIs or UIs, but for internal code good names, asserts and tests are much more important, and make sure that the next developer to work on the code won't break it too badly.