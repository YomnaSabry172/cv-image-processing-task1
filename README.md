# CV Task 1 — Image Processing Web App

A web app for the Computer Vision course (Task 1). Upload a color or grayscale image and apply classic
image-processing operations: noise, low-pass filters, edge detection, histograms and CDF, equalization,
normalization, frequency-domain filters and hybrid images.

- **Backend:** Python, FastAPI, NumPy, SciPy, OpenCV — `backend/`
- **Frontend:** React, Vite, Tailwind CSS, Recharts — `frontend/`
- **Full specification** (rules, file ownership, API contract): [CLAUDE.md](CLAUDE.md)

## Prerequisites

- Python **3.11+**
- Node.js **20+** (with npm)
- Git

## Setup (first time only)

### Backend

```bash
cd backend
python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\Activate.ps1
# Windows (Git Bash):    source .venv/Scripts/activate
# macOS / Linux:         source .venv/bin/activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Run (two terminals)

**Terminal 1 — backend** (with the virtual environment activated):

```bash
cd backend
uvicorn app.main:app --reload
```

API at http://localhost:8000 — interactive docs at http://localhost:8000/docs

**Terminal 2 — frontend:**

```bash
cd frontend
npm run dev
```

Open http://localhost:5173. The sidebar shows **Backend online** when both are running.

## Tests

```bash
cd backend
pytest
```

The convolution tests are skipped until Member B implements `core/convolution.py`.

## Team

| Role | Name | Features |
|------|------|----------|
| Lead | Yomna Sabry | UI, shared utilities, grayscale (7), integration |
| B | `MEMBER_B` | Noise (1), low-pass filters (2), convolution engine |
| C | `MEMBER_C` | Edge detection (3), frequency filters (9), hybrid images (10) |
| D | `MEMBER_D` | Histograms & CDF (4, 8), equalization (5), normalization (6) |

## How to work on your part

1. `git pull`, then create your branch: `feature/noise-filters` (B), `feature/edges-frequency-hybrid` (C), `feature/histograms` (D).
2. Open your files in `backend/app/core/`. Every function you own raises `NotImplementedError("TODO (<you>): ...")` — replace that with your implementation.
3. Run the app. Your page shows **Not implemented yet** until your function works, then shows real results.
4. Only edit files whose header says `# Owner: <you>`. Ask the Lead before changing a shared file.
5. Write your report in `docs/report/report_<role>.md`, then open a pull request.
