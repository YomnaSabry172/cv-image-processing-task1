# Start here

1. Put this `CV_Test_Kit` folder beside your project’s `backend` and `frontend` folders.
2. Read `TEST_PLAN.md` for the 78 manual test cases and precise expected results.
3. The supplied `images` folder has 21 diagnostic files, including invalid inputs.
4. From `backend` with your environment active, run:

```powershell
python -m pytest -q tests ..\CV_Test_Kit\qa_tests --tb=short
```

Test-only tools `pytest` and `httpx` are needed; coordinate installation with the lead under the repository dependency rule. No application source or requirements were changed.

The checked upload produced **220 passes and 10 failures** across existing and new tests. `automated_results.txt` contains the run, and section 7 of the plan explains each failure. Failed tests are intentionally not suppressed.

Use `manual_results.csv` to track browser checks: they are all initially NOT RUN. Browser tests and frontend build were not executed here.

`environment.txt` records this run’s dependencies. `source_snapshot.txt` identifies the archive. `generate_test_images.py` recreates synthetic fixtures if required.
