# Work log

- I started by testing binary/number conversions, the most critical part of the data flow, to ensure information consistency.

- I initially used Python's default data structures, especially lists, and planned to replace them with dedicated classes later.

- After binary encoding/decoding, I wrote triangulation tests for all cases in the plan and a function to check that each triangle uses valid, distinct, non-collinear vertices.

- I then wrote integration tests, starting with the `point_set_manager` endpoint return codes.

- I defined specific exceptions instead of relying on the default `Exception`, so tests cannot pass for the wrong error; for example, I used `InvalidPointSetError`.


- I decided to automate validation with the GitHub Actions workflow
`.github/workflows/ci.yml`, which runs on every `push` and `pull_request`.
I configured it to install the project dependencies, run the tests and
coverage check, perform the Ruff quality check, and generate the documentation. This way, I can check the tests and documentation automatically after each
code change and before merging a pull request.