# Student Guide — FileAI (AI-Powered Personal Digital File Organizer)

This guide is for **every member of Group 4**, including anyone who has never run a Python or React project before. Follow it from top to bottom the first time. After that you only need [Part 5 — Run the app every day](#5-run-the-app-every-day).

**Contents**

1. [What is this project?](#1-what-is-this-project)
2. [How the system works (in plain words)](#2-how-the-system-works-in-plain-words)
3. [Install the tools (once per computer)](#3-install-the-tools-once-per-computer)
4. [Get the code and set it up (once)](#4-get-the-code-and-set-it-up-once)
5. [Run the app every day](#5-run-the-app-every-day)
6. [Use the app — a guided tour](#6-use-the-app--a-guided-tour)
7. [5-minute demo script for the presentation](#7-5-minute-demo-script-for-the-presentation)
8. [Stop the app](#8-stop-the-app)
9. [Troubleshooting](#9-troubleshooting)
10. [Where things are in the code](#10-where-things-are-in-the-code)
11. [Run the tests](#11-run-the-tests)
12. [Optional extras: OCR, OpenAI, AWS S3](#12-optional-extras-ocr-openai-aws-s3)
13. [Working together with Git](#13-working-together-with-git)
14. [Glossary](#14-glossary)

---

## 1. What is this project?

**FileAI** is a website where you upload your documents (PDF, Word, text files, photos of documents) and the system **organises them for you**:

- it reads the text inside the file,
- works out what kind of document it is (assignment, invoice, resume, …),
- suggests a **clear filename** and a **folder** (e.g. `University / Year 2 / Semester 1 / Database Systems`),
- writes a short **summary** and **keywords**,
- warns you if you already have the **same or a very similar file**,
- and lets you **find files by asking in plain English**, e.g. *"Find my Semester 1 Database assignment"*.

You always stay in control: nothing is saved until you **approve** (or edit) the AI's suggestions.

This is our NIT3003/NIT3004 capstone project. The full design is in the [`docs/`](docs/README.md) folder.

## 2. How the system works (in plain words)

The project has **three parts** that run at the same time:

| Part | Folder | Technology | What it does | Address |
|---|---|---|---|---|
| **Frontend** (what you see) | `frontend/` | React + Bootstrap | The web pages: login, upload, search… | <http://localhost:5173> |
| **Backend** (the brain) | `backend/` | Python + Flask | Checks files, reads text, runs the AI, answers searches | <http://127.0.0.1:5000/api> |
| **Database** (the memory) | — | MySQL (via Laragon) | Stores users, document details, folders, keywords | port 3306 |

The uploaded files themselves are saved in `backend/uploads/` (or in AWS S3 if we switch that on).

**What happens when you upload a file:**

```text
You drop a file ─► Backend checks it (type, size, not broken, not a duplicate)
                ─► Saves the file
                ─► Reads the text (PDF reader / Word reader / OCR for images)
                ─► AI suggests category, title, summary, keywords, filename, folder
                ─► Checks for similar documents
                ─► You review and click "Approve & Save"
                ─► The document is filed and searchable
```

**The AI:** by default the project uses its **own built-in AI analyser** that runs on your computer. It needs **no internet and no API key**, so the demo always works. If we get an OpenAI API key, we can switch to GPT with one setting (see [Part 12](#12-optional-extras-ocr-openai-aws-s3)).

## 3. Install the tools (once per computer)

Install these four things. Accept the default options unless the table says otherwise.

| Tool | Why we need it | Download | Important |
|---|---|---|---|
| **Laragon** (Windows) | Gives us MySQL with one click | <https://laragon.org/download/> (Full edition) | macOS: use XAMPP or `brew install mysql` instead |
| **Python 3.11 or newer** | Runs the backend | <https://www.python.org/downloads/> | On the first installer screen, **tick "Add python.exe to PATH"** |
| **Node.js LTS** (20 or newer) | Runs the frontend | <https://nodejs.org/> | Choose the **LTS** version |
| **Git** | Downloads the code and shares changes | <https://git-scm.com/downloads> | Defaults are fine |

**Check that everything installed.** Open **Command Prompt** (press the Windows key, type `cmd`, press Enter) and run these one by one:

```bash
python --version
```

```bash
node --version
```

```bash
git --version
```

Each should print a version number (e.g. `Python 3.13.1`, `v22.11.0`). If you see *"is not recognized"*, see [Troubleshooting](#9-troubleshooting).

## 4. Get the code and set it up (once)

### 4.1 Download the code

In Command Prompt, go to where you keep projects (for example your Documents folder) and clone the repository:

```bash
cd %USERPROFILE%\Documents
```

```bash
git clone https://github.com/YousufMunirKhan/filemanager.git
```

This creates a folder called `filemanager`. Open it in File Explorer.

### 4.2 Start MySQL

Open **Laragon** and click **Start All**. Wait until MySQL shows as running (green).

### 4.3 Run the setup script (Windows — the easy way)

In the `filemanager` folder, **double-click `setup.bat`**. It will:

1. create a Python environment and install the backend packages (takes a few minutes the first time),
2. create the settings file `backend\.env`,
3. create the `file_organizer` database and its tables in MySQL,
4. create a **demo account with 9 sample documents** already organised by the AI,
5. install the frontend packages.

When it says **"Setup complete"**, you are done. If it stops with an error, read the message and check [Troubleshooting](#9-troubleshooting).

> **MySQL with a password?** Laragon and XAMPP use user `root` with **no password** by default, which is what the settings file expects. If your MySQL has a password, open `backend\.env` in a text editor and change the line to
> `DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@127.0.0.1:3306/file_organizer?charset=utf8mb4`
> then run `setup.bat` again.

### 4.4 macOS / Linux — the easy way

Start MySQL first (`brew services start mysql`, or XAMPP / MAMP), then in a terminal opened in the project folder:

```bash
./setup.sh        # once
./start-dev.sh    # every day (Ctrl+C stops it)
```

`start-dev.sh` runs the backend on port **5001** on macOS (AirPlay uses 5000) and opens <http://localhost:5173>.
If it says Python is too old: `brew install python@3.12`, then `PYTHON=python3.12 ./setup.sh`.

### 4.5 Manual setup (if you prefer typing commands)

Backend — in a terminal opened in the project folder:

```bash
cd backend
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\python -m pip install -r requirements.txt
copy .env.example .env
.venv\Scripts\python -m flask --app run.py init-db
.venv\Scripts\python -m flask --app run.py seed-demo
```

macOS / Linux (use `python3` if `python` is not found):

```bash
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
.venv/bin/python -m flask --app run.py init-db
.venv/bin/python -m flask --app run.py seed-demo
```

Frontend — in a terminal opened in the project folder:

```bash
cd frontend
npm install
```

## 5. Run the app every day

1. Open **Laragon** → **Start All** (MySQL must be running).
2. In the project folder, **double-click `start-dev.bat`**.
   - Two black windows open: **FileAI API** (backend) and **FileAI Web** (frontend). **Keep both open** while you use the app.
   - After a few seconds your browser opens <http://localhost:5173>.
3. Sign in with the demo account:
   - **Email:** `demo@fileai.test`
   - **Password:** `Demo@12345`
   - **Verification code:** sign-in has a second step (two-step verification): a 6-digit code is **emailed**.
     `demo@fileai.test` is not a real inbox, so once the email server is set up (Part 12) sign in with your own
     email instead. To get the sample files in your own account run, in `backend`:
     `flask --app run.py seed-demo --email you@gmail.com --password "YourPassw0rd!"`.
     The code is only ever emailed. `demo@fileai.test` is not a real inbox, so move the demo account to your own
     email once: in `backend` run `.venv/bin/python -m flask --app run.py change-email demo@fileai.test you@gmail.com`
     (Windows: `.venv\Scripts\python ...`).

**Manual way** (or on macOS) — use two terminals:

Terminal 1 (backend):

```bash
cd backend
.venv\Scripts\python -m flask --app run.py run --port 5000
```

(macOS: `.venv/bin/python -m flask --app run.py run --port 5000`)

Terminal 2 (frontend):

```bash
cd frontend
npm run dev
```

Then open <http://localhost:5173> in Chrome, Edge or Firefox.

**Quick health check:** open <http://127.0.0.1:5000/api/health>. You should see `"status": "ok"`. If not, the backend isn't running.

## 6. Use the app — a guided tour

The layout works like **OneDrive**: a **+ Create or upload** button at the top of the left menu (Upload files / New folder), then Home, My files, AI Search, Review Queue and Recycle bin.

| Page (left menu) | What to try |
|---|---|
| **Home** | Ask-AI search box, totals, **Your folders** (each with an **AI summary** button) and **Recent files** (like OneDrive) with *Filter by name* and a **⋯** menu: Open, Download, Rename, Delete |
| **+ Create or upload → Upload files** | Drag a PDF/DOCX/TXT/PNG/JPG onto the box (or click **Browse files**). Watch the progress bar, then "Analysis ready" — the row says which folder the AI suggests → **Review** |
| **Review Queue** | Documents waiting for your approval. The demo account has one: `Database_Assignment_v2.txt`, flagged as **97% similar** to an existing file |
| **AI review page** | The **AI suggested folder** card lists your best **existing** folders with the reason (e.g. *"1 similar document is already here"*); the best one is already chosen. Check the title, filename, category, keywords and summary, then **Approve & Save**, or **Discard upload** |
| **My files** | The file explorer: click folders to open them, go back with the breadcrumb (*My files / University / Year 2*), list or tiles view, **New folder**, **Summarise with AI**, **Rename**, **Delete** |
| **AI Search** | Type a question like *Find my Semester 1 Database assignment*, *invoices*, *my resume*, *flight booking*. Matching **folders** are shown first — click **Open** to jump into the folder |
| **Recycle bin** | Deleted files wait here. **Restore** puts a file back in its old folder; **Empty recycle bin** deletes for good |
| **All documents** | All your files in one list. Filter by category, type or folder; sort by date or name |
| **Document details** | Preview (PDF/images shown directly, Word/TXT as text), all AI metadata, and **Edit / Rename / Move / Download / Move to Recycle bin** |
| **Categories** | Documents grouped by category |
| **Profile & Settings** | Change name, email, password; see storage use and which AI is running |

**Try these on purpose (good for the demo):**

- Upload the **same file twice** → you get *"You already have this file"* with **Upload anyway / Cancel**.
- Upload a file with the wrong type (e.g. `.exe`) → it is rejected.
- **Register** a new account with a weak password → the checklist shows which rules are missing (8+ characters, uppercase, lowercase, number, special character). With a good password you get a **"Confirm your email"** step: type the 6-digit code and the new account is created and signed in.
- Type a wrong verification code → *"That code is not correct"*. After 5 wrong codes you must ask for a new one.
- Upload a new database document (e.g. *"Unit: NIT2102 Database Systems … SQL lab"*) → the AI suggests the **existing** `University / Year 2 / Semester 1 / Database Systems` folder.
- **Delete** a folder in My files → its documents go to the **Recycle bin** → **Restore** brings them back (the folders are re-created).
- Log in with a wrong password 5 times → the account is locked for 5 minutes (security feature).
- Log in as a second user → you cannot see the first user's files.

**Making your own test files:** a Word or text file with lines like *"Unit: NIT2102 Database Systems"*, *"Semester 1"*, *"Year 2"*, *"Assignment"* will be filed under `University / Year 2 / Semester 1 / Database Systems`. Invoices with a company name and a "Total" amount go to `Finance / Invoices / <year>`.

## 7. 5-minute demo script for the presentation

Practise this once before the presentation. Start the app (Part 5) and log in **before** you begin presenting.

| Time | Show | Say |
|---|---|---|
| 0:00 | Sign-in with the code | "Sign-in is two-step: after the password, a 6-digit code is emailed. Only someone who can read that inbox can sign in." |
| 0:30 | Home | "Like OneDrive, Home shows my folders and my recent files. I can rename, delete or ask the AI to summarise a folder." → click **AI summary** on *University* |
| 1:00 | Upload Files → drop a new file | "When I upload a file, the backend checks it, extracts the text and runs our AI analysis in the background." |
| 1:30 | Review page | "The AI recommends one of my **existing** folders and tells me why — here, a similar document is already in Database Systems. Nothing is saved until I approve." → **Approve & Save** |
| 2:15 | Upload the same file again | "Duplicate detection: SHA-256 hashing catches exact copies." |
| 2:45 | Review Queue → `Database_Assignment_v2.txt` | "Edited copies are caught too — this one is 97% similar to an existing assignment." |
| 3:15 | AI Search → *Find my Semester 1 Database assignment* | "Natural-language search finds documents by meaning and keywords, in milliseconds." |
| 4:00 | My files → open folders, **Delete** a file → Recycle bin → **Restore** | "My files works like OneDrive: breadcrumb, rename, delete and a Recycle bin, so nothing is lost by mistake." |
| 4:30 | Settings → AI & Privacy | "Security: BCrypt passwords, JWT sessions, per-user access, signed download links. The AI runs locally, so no document text leaves the server." |

Key numbers you can quote (from our tests, see [Testing Strategy](docs/11-testing-strategy.md)): upload confirmed in **~0.1 s** (target 3 s), AI processing **~0.5 s** (target 30 s), search **20–60 ms** (target 2 s), **99 backend + 93 frontend automated tests** passing, **9/9** sample documents classified correctly.

## 8. Stop the app

- Close the two black windows (**FileAI API** and **FileAI Web**), or press `Ctrl + C` in each terminal.
- In Laragon click **Stop** (optional).

Your data stays in MySQL and `backend/uploads/` for next time.

## 9. Troubleshooting

| Problem | What it means | Fix |
|---|---|---|
| `'python' is not recognized` | Python is not on PATH | Re-run the Python installer → **Modify** → tick **Add Python to environment variables**. Or reinstall and tick **Add python.exe to PATH**. Close and reopen Command Prompt. |
| `'npm' is not recognized` | Node.js not installed or terminal opened before install | Install Node.js LTS, then **close and reopen** the terminal |
| `Can't connect to MySQL server` / error **2003**, or the website says *"The server can't reach its database"* | MySQL isn't running | Open Laragon → **Start All** (macOS: `brew services start mysql`), then try again |
| Something doesn't work and you don't know why | — | Look at the **backend window**: when it starts it prints a short report (settings file, database, sign-in codes, AI, OCR) with what to fix |
| Settings page says *Local model* / OCR *Not installed on the server* | No OpenAI key in `backend/.env` | Add `OPENAI_API_KEY=sk-...` to `backend/.env` (the file must be called exactly `.env`, inside `backend`) and restart the backend |
| `Access denied for user 'root'` / error **1045** | Your MySQL has a password | Put it in `DATABASE_URL` in `backend\.env` (see [4.3](#43-run-the-setup-script-windows--the-easy-way)) |
| Website says *"Can't reach the FileAI server"* | Backend is not running | Start it (Part 5) and check <http://127.0.0.1:5000/api/health> |
| `Port 5173 is already in use` | The frontend is already running in another window | Close the other **FileAI Web** window, or just use the one already open |
| `Address already in use` on port 5000 | Backend already running, or (macOS) AirPlay uses port 5000 | Close the other backend window. On macOS run the backend with `--port 5001` and start the frontend with `VITE_API_PROXY_TARGET=http://127.0.0.1:5001 npm run dev` |
| PowerShell: *"running scripts is disabled on this system"* | PowerShell blocks `Activate.ps1` | Use **Command Prompt** instead, or the commands in this guide that call `.venv\Scripts\python` directly (no activation needed) |
| Image or scanned PDF shows *"OCR is not installed"* | Tesseract isn't installed | Expected without OCR. Install Tesseract (Part 12), or type the details in yourself and approve |
| *"Too many failed sign-in attempts"* | Security lockout after 5 wrong passwords | Wait 5 minutes, or restart the backend window |
| *"Your session has expired"* | Login lasts 30 minutes | Sign in again |
| Where is my sign-in code? | It is emailed (check the spam folder too) | *"The email server isn't set up"* means `SMTP_HOST` is empty in `backend\.env`: see Part 12, then restart the backend |
| *"We couldn't send the verification email"* | The SMTP settings in `backend\.env` are wrong | Check `SMTP_HOST`, `SMTP_USERNAME` and the Gmail **app password**, then run `flask --app run.py send-test-email you@gmail.com` |
| *"This code has expired"* / *"Too many wrong codes"* | Codes last 10 minutes and allow 5 tries | Click **Resend code** |
| `Unknown column 'files.deleted_at'` | Database made by v0.1 | Restart the backend (it upgrades the database itself), or run `.venv\Scripts\python -m flask --app run.py init-db` once |
| Demo account missing / want a clean start | — | In `backend`: `.venv\Scripts\python -m flask --app run.py init-db --drop` (type `y` to confirm — **deletes all data**), then `... seed-demo` |
| `setup.bat` window closes immediately | Error before the first message | Open Command Prompt in the project folder and type `setup.bat` to read the error |

Still stuck? Copy the **full error message** from the black window and send it to the team chat.

## 10. Where things are in the code

| I want to change… | Look in |
|---|---|
| How a page looks or behaves | `frontend/src/pages/` (one file per page, e.g. `UploadPage.jsx`, `SearchPage.jsx`) |
| Colours, spacing, fonts | `frontend/src/styles/app.css` |
| Sidebar and top bar | `frontend/src/components/layout/` |
| How the frontend calls the backend | `frontend/src/api/` |
| API endpoints (URLs) | `backend/app/api/` (`auth.py`, `documents.py`, `search.py`, …) |
| Allowed file types and size checks | `backend/app/services/validation.py` |
| Reading text from PDF / Word / images | `backend/app/services/extraction.py` |
| AI rules: categories, titles, folders, filenames | `backend/app/services/ai/local.py` |
| OpenAI (GPT) version of the AI | `backend/app/services/ai/openai_provider.py` |
| Search ranking | `backend/app/services/search.py` |
| The processing steps after upload | `backend/app/services/pipeline.py` |
| Database tables | `backend/app/models.py` and `database/schema.sql` |
| Demo account and sample documents | `backend/app/demo.py` |
| Settings (database, AI, upload size) | `backend/.env` (template: `backend/.env.example`) |

Design documents for each part: [Architecture](docs/04-system-architecture.md) · [Database](docs/05-database-design.md) · [API](docs/06-api-specification.md) · [UI](docs/07-ui-design.md).

## 11. Run the tests

Backend (no MySQL needed — tests use a temporary database):

```bash
cd backend
.venv\Scripts\python -m pytest
```

Frontend:

```bash
cd frontend
npm run test:run
```

Both should end with everything **passed**. Run them before you push changes.

## 12. Optional extras: OCR, OpenAI, AWS S3

All of these are switched on in `backend\.env`. **Restart the backend window after changing `.env`.**

**OCR (read text from photos and scanned PDFs)**

1. Install Tesseract for Windows: <https://github.com/UB-Mannheim/tesseract/wiki>
2. In `backend\.env` set
   `TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe`
3. Restart the backend. **Profile & Settings → AI & Privacy** should now show OCR as available.

**Real emails for the sign-in codes (two-step verification)**

1. Use a Gmail account for the project. Turn on **2-Step Verification** for it, then create an **App password**
   (Google Account → Security → App passwords). It is a 16-character password just for this app.
2. In `backend\.env` set

   ```text
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=yourproject@gmail.com
   SMTP_PASSWORD=the16characterapppassword
   ```

   A hosting mailbox works too, e.g. Hostinger: `SMTP_HOST=smtp.hostinger.com`, `SMTP_PORT=465`,
   `SMTP_USE_SSL=true`, the full email address as `SMTP_USERNAME`, and `MAIL_FROM="FileAI <that address>"`.
   Put the password in single quotes if it has symbols: `SMTP_PASSWORD='p|a:s~s'`.
3. Check it: `flask --app run.py send-test-email you@gmail.com` (in `backend`, with the venv on).
4. Restart the backend. Codes are now emailed and are **never shown on screen**.
   To switch two-step verification off completely (not recommended): `TWO_FACTOR_ENABLED=false`.
   Demo without any email server only: `EMAIL_DEMO_MODE=true` shows the code on screen instead (off by default).

**OpenAI GPT instead of the built-in AI**

```text
OPENAI_API_KEY=sk-...your key...
```

GPT is used automatically once a key is set (`AI_PROVIDER=local` forces the built-in AI). If the API fails, the app automatically falls back to the built-in AI. Never commit your real key — `.env` is ignored by Git on purpose.

**AWS S3 instead of the local `uploads` folder**

```text
STORAGE_BACKEND=s3
S3_BUCKET_NAME=your-bucket
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=ap-southeast-2
```

## 13. Working together with Git

Short version (details in [CONTRIBUTING.md](CONTRIBUTING.md)):

```bash
git checkout develop
git pull
git checkout -b feature/my-change
```

Make your changes, run the tests, then:

```bash
git add .
git commit -m "feat(upload): short description of the change"
git push -u origin feature/my-change
```

Open a **Pull Request** into `develop` on GitHub and ask a teammate to review it. `main` is kept for working, demo-ready versions.

**Never commit:** `backend/.env`, API keys, passwords, real personal documents, `node_modules/` or `.venv/` (the `.gitignore` file already blocks these).

## 14. Glossary

| Term | Meaning |
|---|---|
| **Frontend** | The part that runs in the browser (React). |
| **Backend** | The server program that does the work (Flask, Python). |
| **API** | The list of URLs the frontend calls to ask the backend for something, e.g. `POST /api/search`. |
| **Database (MySQL)** | Where users, document details, folders and keywords are stored in tables. |
| **OCR** | Optical Character Recognition — turning a picture of text into real text (Tesseract). |
| **NLP** | Natural Language Processing — computers working with human language (keywords, summaries, search). |
| **Embedding** | A list of numbers that represents a document's content, so similar documents have similar numbers. Used for search and similar-file detection. |
| **SHA-256 hash** | A fingerprint of a file. Two identical files always have the same hash, which is how exact duplicates are found. |
| **JWT** | JSON Web Token — the "ticket" the backend gives you at login; the frontend sends it with every request. Expires after 30 minutes. |
| **BCrypt** | A slow, salted way of storing passwords so they can't be read even if the database leaks. |
| **Virtual environment (`.venv`)** | A private folder of Python packages just for this project. |
| **`.env` file** | Local settings (database address, API keys). Not shared in Git. |
| **Seed / demo data** | Example account and documents created by `seed-demo` so the app isn't empty. |
