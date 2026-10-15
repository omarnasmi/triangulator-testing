# Work log

- I started by testing binary/number conversions, the most critical part of the data flow, to ensure information consistency.

- I initially used Python's default data structures, especially lists, and planned to replace them with dedicated classes later.

- After binary encoding/decoding, I wrote triangulation tests for all cases in the plan and a function to check that each triangle uses valid, distinct, non-collinear vertices.

- I then wrote integration tests, starting with the `point_set_manager` endpoint return codes.

- I defined specific exceptions instead of relying on the default `Exception`, so tests cannot pass for the wrong error; for example, I used `InvalidPointSetError`.