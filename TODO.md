1. Delete `data_transformer.py`.
2. config module?
3. Improve code quality:
    - consistent type hints and docstrings
    - add logging
        - logging config
4. Write unit tests again. 
    - Make them nicer.
    - split unit/integration/e2e
    - adapt docker setup: test database etc
5. Rewrite DAG to be easily distributed. Maybe ask GPT about high level design of distributed system task processing.
6. Pre-commit hooks for code quality stuff.