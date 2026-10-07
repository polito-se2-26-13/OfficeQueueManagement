# Office Queue Management

Software Engineering II, PoliTo 2026/27, team 13.

```
client/   frontend, React + Vite
server/   backend, FastAPI + SQLAlchemy + SQLite
```

## Run the backend

Windows, in PowerShell:

```
cd server
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

If PowerShell says that running scripts is disabled, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and open a new terminal. If `python` opens the Microsoft Store, use `py` instead.

macOS and Linux:

```
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The API runs on http://localhost:8000 and its documentation on http://localhost:8000/docs.

## Run the frontend

```
cd client
npm install
npm run dev
```

The app runs on http://localhost:5173. Calls to `/api/...` are forwarded to the backend, so start both.

## Tests

With the virtual environment active:

```
cd server
pytest
```

## Branches

- `main` holds what we show at the sprint review. It only receives the merge of `dev` at the end of each sprint.
- `dev` is where the work comes together. Nobody pushes to it directly.
- Every task gets its own short branch, created from an up to date `dev` and named after its YouTrack card: `OQM-<number>-<short-description>`, for example `OQM-15-post-tickets`.
- Commit messages start with the card ID too, for example `OQM-15 add POST /tickets`.
- When the task is done, open a pull request into `dev`. Another member reviews and approves it, then it is merged and the branch is deleted.
