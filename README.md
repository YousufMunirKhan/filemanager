# AI-Powered Personal Digital File Organizer

> An intelligent web application that reads your documents, organises them automatically, and lets you find them by asking in plain English.

**NIT3003 / NIT3004 IT Capstone Project — Group 4, Victoria University**

> 👉 **New to the project? Start with the [Student Guide](STUDENT_GUIDE.md)** — what to install, how to run the app step by step, a demo script for the presentation, and fixes for common errors.

| | |
|---|---|
| **Status** | ✅ Proposal and presentation (NIT3003) · ✅ Working application v0.2 — reviewer feedback implemented (see [What's new in v0.2](#whats-new-in-v02-reviewer-feedback)) |
| **Stack** | React.js · Bootstrap · Python Flask · MySQL · AWS S3 · Tesseract OCR · PyMuPDF · python-docx · OpenAI GPT / Hugging Face |
| **Docs** | [`docs/`](docs/README.md) |

---

## The problem

Students and professionals keep thousands of files across laptops and cloud drives. Organising them means creating folders by hand, renaming files, and remembering exact filenames to search. Scanned documents can't be searched at all, and duplicates pile up.

## The solution

Upload a file and the system does the organising:

1. **Extracts the text** from PDF, DOCX, TXT, PNG or JPG (OCR for scans and images)
2. **Understands it with AI** — category, title, keywords and a short summary
3. **Suggests a filename and folder**, e.g. `University ▸ Year 2 ▸ Semester 1 ▸ Database Systems`
4. **Warns about duplicates** — identical files (SHA-256) and edited copies (similarity)
5. **Lets you approve or edit** every suggestion before saving
6. **Finds files by meaning** — *"Find my Semester 1 Database assignment"*

```text
Upload ─► Validate ─► Extract / OCR ─► AI analysis ─► Metadata ─► Duplicate check ─► Review ─► Store ─► Search
```

## What's new in v0.2 (reviewer feedback)

| Feedback from the demonstration | What we built |
|---|---|
| Improve account registration / login security | **Two-step verification**: a 6-digit code is emailed at sign-up (the account is only created once the email is confirmed) and at every sign-in. Codes are only sent by email (Gmail or any SMTP mailbox, SSL or STARTTLS); they are never shown on screen. |
| Interface similar to OneDrive | **OneDrive-style layout**: "+ Create or upload" button, **Home**, **My files** explorer (breadcrumb, list / tiles view, filter by name, ⋯ menu) and a **Recycle bin** with restore. |
| Dashboard showing files and folders, search, rename, delete, summarise | **Home** now lists **Your folders** and **Recent files** (like OneDrive), with an AI search box. Files and folders can be **renamed**, **deleted** (to the Recycle bin) and any folder can be **summarised by AI**. |
| Improve AI recommendation | When a file is uploaded the AI **suggests one of your existing folders** (by similar documents, folder names and its own analysis) and explains why; a new folder is only suggested when nothing fits. |
| AI search should take you to the folder | **AI Search also finds folders** and opens them in My files. |

## Screenshots

| Home (v0.2) — folders, recent files, AI search | AI suggests an existing folder (v0.2) |
|---|---|
| ![Home](docs/images/manual/04-home.jpg) | ![AI suggested folder](docs/images/manual/14-review-ai-folder.jpg) |
| **My files explorer (v0.2)** | **AI folder summary (v0.2)** |
| ![My files](docs/images/manual/11-myfiles-menu.jpg) | ![Folder summary](docs/images/manual/08-folder-summary.jpg) |
| **Dashboard (v0.1)** | **AI review — similar file warning (v0.1)** |
| ![Dashboard](docs/images/app-dashboard.jpg) | ![AI review](docs/images/app-review.jpg) |
| **Natural-language search** | **Upload queue (duplicate + invalid file)** |
| ![Search](docs/images/app-search.jpg) | ![Upload](docs/images/app-upload.jpg) |

## Key features

| Feature | Requirement |
|---|---|
| Secure registration and login (BCrypt + JWT) with two-step email verification | FR-01 |
| Drag-and-drop multi-format upload | FR-02 |
| AI document classification | FR-03 |
| Automatic title, keywords and summary | FR-04 |
| Filename and folder recommendations (prefers your existing folders) | FR-05 |
| OneDrive-style My files, Recycle bin, folder rename / delete / AI summary | FR-05, FR-12 |
| Natural-language (semantic) search | FR-06 |
| Exact and similar duplicate detection | FR-07 |
| Secure, per-user storage on AWS S3 | FR-11 |

## Architecture

![System architecture](docs/images/system-architecture.png)

| Layer | Technology |
|---|---|
| User interface | React.js + Bootstrap |
| API | Python Flask (REST, JSON, JWT) |
| AI and extraction | PyMuPDF, python-docx, Tesseract OCR, OpenAI GPT / Hugging Face |
| Data | MySQL 8 (metadata), AWS S3 (files) |

Details: [System Architecture](docs/04-system-architecture.md) · [Database Design](docs/05-database-design.md) · [API Specification](docs/06-api-specification.md)

## Repository structure

```text
.
├── README.md                  ← you are here
├── STUDENT_GUIDE.md           ← step-by-step guide: install, run, demo, troubleshooting
├── setup.bat                  ← one-time setup on Windows
├── start-dev.bat              ← start backend + frontend on Windows
├── CONTRIBUTING.md            ← Git workflow, branches, commits, PRs
├── CHANGELOG.md
├── docs/                      ← all project documentation
│   ├── 01-project-overview.md
│   ├── 02-requirements-specification.md
│   ├── 03-use-cases.md
│   ├── 04-system-architecture.md
│   ├── 05-database-design.md
│   ├── 06-api-specification.md
│   ├── 07-ui-design.md
│   ├── 08-algorithms-pseudocode.md
│   ├── 09-project-plan.md
│   ├── 10-risk-management.md
│   ├── 11-testing-strategy.md
│   ├── 12-references.md
│   └── images/
├── frontend/                  ← React + Vite + Bootstrap web app
│   └── src/                   ← pages, components, API client
├── backend/                   ← Flask REST API
│   ├── app/                   ← API, AI pipeline, models, services
│   ├── tests/                 ← pytest suite (99 tests)
│   ├── requirements.txt
│   └── .env.example
├── database/
│   └── schema.sql             ← MySQL schema
└── .github/
    └── pull_request_template.md
```

## Documentation

| | |
|---|---|
| **[User Manual (PDF)](docs/user-manual/FileAI-User-Manual.pdf)** | How to use FileAI, step by step with screenshots (v0.2) |
| [Project Overview](docs/01-project-overview.md) | Problem, market, competitors, aim, objectives, scope |
| [Requirements](docs/02-requirements-specification.md) | Functional and non-functional requirements, traceability |
| [Use Cases](docs/03-use-cases.md) | UC-01 to UC-10 |
| [System Architecture](docs/04-system-architecture.md) | Layers, pipeline, sequence diagrams, security |
| [Database Design](docs/05-database-design.md) | ER diagram and tables |
| [API Specification](docs/06-api-specification.md) | All REST endpoints with examples |
| [UI Design](docs/07-ui-design.md) | Screens and prototype screenshots |
| [Algorithms and Pseudocode](docs/08-algorithms-pseudocode.md) | Core procedures |
| [Project Plan](docs/09-project-plan.md) | Team, milestones, Gantt, sprints |
| [Risk Management](docs/10-risk-management.md) | Risk register |
| [Testing Strategy](docs/11-testing-strategy.md) | Test plan and current results |
| [References](docs/12-references.md) | APA 7th |

## Getting started

You need **Python 3.11+**, **Node.js 20+** and **MySQL 8** (Laragon or XAMPP is fine). No API keys are needed: the built-in AI analyser runs offline.

### Quick start on Windows

1. Start MySQL (e.g. *Start All* in Laragon).
2. Double-click **`setup.bat`** once — installs everything, creates the database and a demo account.
3. Double-click **`start-dev.bat`** — starts both servers and opens <http://localhost:5173>.
4. Sign in with **demo@fileai.test** / **Demo@12345**.

### Quick start on macOS / Linux

1. Start MySQL (`brew services start mysql`, or XAMPP / MAMP).
2. In a terminal in the project folder: **`./setup.sh`** once.
3. Then **`./start-dev.sh`** — starts both servers (the API uses port 5001 on macOS, because AirPlay uses 5000) and opens <http://localhost:5173>.
4. Sign in with **demo@fileai.test** / **Demo@12345**.

### What works straight after cloning

`backend/.env` holds passwords and keys, so it is **not** in Git. Without it the app still runs:

- **Sign-in codes:** only ever emailed, never shown on screen. Put the `SMTP_*` settings in `backend/.env`; without them sign-up and sign-in stop with "the email server isn't set up". `demo@fileai.test` is not a real inbox: move it to yours with `flask --app run.py change-email demo@fileai.test you@gmail.com`.
- **AI:** the built-in local analyser. Put `OPENAI_API_KEY=...` in `backend/.env` to use GPT for analysis, folder choice and reading scans/photos.
- **Database:** created automatically on first start, if MySQL is running.

Settings pasted above or below the template lines both count. When the backend starts it prints a short report of what it found — read it first if something doesn't work. Share keys privately (never commit them: this repository is public and OpenAI switches off keys published on GitHub).

### Manual setup

**1. Start MySQL** (e.g. *Start All* in Laragon).

**2. Backend** (first terminal):

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
flask --app run.py init-db
flask --app run.py seed-demo
flask --app run.py run --port 5000
```

On macOS use `source .venv/bin/activate` and `cp .env.example .env`. If your MySQL user has a password, edit `DATABASE_URL` in `backend/.env`.

**3. Frontend** (second terminal):

```bash
cd frontend
npm install
npm run dev
```

**4. Open <http://localhost:5173>** and sign in with the demo account **demo@fileai.test** / **Demo@12345**, or register a new account.

Optional extras:

- **OCR for scans and photos:** install [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) and set `TESSERACT_CMD` in `backend/.env`.
- **OpenAI GPT analysis:** set `OPENAI_API_KEY` in `backend/.env` (GPT is used automatically when a key is set).
- **AWS S3 storage:** set `STORAGE_BACKEND=s3`, `S3_BUCKET_NAME` and AWS credentials.

Details: [Backend README](backend/README.md) · [Frontend README](frontend/README.md)

## Running the tests

```bash
cd backend && pytest --cov=app        # 120 tests, no MySQL needed
cd frontend && npm run test:run       # 93 component and helper tests (Vitest)
```

## Project timeline

| Milestone | Description | Status |
|---|---|---|
| M1 | Project proposal completed (NIT3003) | ✅ |
| M2 | Oral presentation (NIT3003) | ✅ |
| M3 | 80% system completion checkpoint (NIT3004) | ⏳ Core features already implemented (v0.1) |
| M4 | Final submission and demonstration (NIT3004) | ⏳ Testing with real users, OCR, polish |

See the [Project Plan](docs/09-project-plan.md) for the Gantt chart and sprint plan.

## Team

| Name | Student ID |
|---|---|
| Al Shahariar | s8159455 |
| Hassan Zaheer | s8149265 |
| Sebagat Selim | s8131475 |
| Royal Dhakal | s8160992 |

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before your first commit. In short: branch from `develop`, use `feature/...` branch names, open a pull request, and get one review before merging.

## Licence

Academic project for Victoria University. No open-source licence has been chosen yet; all rights reserved by the authors.
