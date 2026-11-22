# Changelog

All notable changes to this project are recorded here. Format based on [Keep a Changelog](https://keepachangelog.com/).

## [0.3.2] — 2026-11-22

### Changed
- Sign-in codes are only emailed again, never shown on screen: `EMAIL_DEMO_MODE` defaults to `false` (as in 0.3.0).

### Added
- `flask --app run.py change-email OLD NEW` moves an account (e.g. `demo@fileai.test`) to a real inbox, keeping its password and documents.
- `backend/settings_files.py`: settings pasted above or below the template lines both count (a typed value beats the `.env.example` value, which beats an empty one), also when `flask run` already loaded the file; values from a second `.env` fill the gaps.

### Fixed
- Email over SSL failed on macOS with python.org Python (no root certificates): the SMTP connection also trusts `certifi`'s certificates.

## [0.3.1] — 2026-11-22

A fresh clone works without any setup (problems reported by students on macOS).

### Added
- `setup.sh` and `start-dev.sh` for macOS / Linux (the API runs on port 5001 on macOS, where AirPlay uses 5000).
- Startup report: when the backend starts it prints which settings file it read, whether the database works, how sign-in codes are delivered, and which AI / OCR is in use, with what to do about anything missing.
- 5 new backend tests (120 in total).

### Changed
- Without an email server, sign-up and sign-in work in demo mode again (code shown on screen and printed in the backend window): `EMAIL_DEMO_MODE` now defaults to `true`. It still has no effect once `SMTP_HOST` is set; set `EMAIL_DEMO_MODE=false` on a real server.
- `AI_PROVIDER` left empty means OpenAI when `OPENAI_API_KEY` is set, otherwise local — adding the key is enough.
- The backend also reads `.env` from the project folder or `backend/.env.txt` (common mistakes), and says so.
- The MySQL database and its tables are created on first start if missing (no `init-db` needed); if MySQL isn't running yet it retries on the next request.

### Fixed
- Database problems (MySQL not running, wrong password, missing database) showed "Something went wrong on the server"; they now answer `503 DATABASE_UNAVAILABLE` with a clear message and a one-line hint in the backend window.

## [0.3.0] — 2026-11-20

Real email codes, GPT folder choice and GPT reading of scans.

### Added
- GPT chooses the folder: the OpenAI analyser gets the user's folder list and returns `existing_folder` (copied exactly) plus a one-line `folder_reason`. When GPT did the analysis its choice counts 60% in the folder ranking (similar documents 25%, folder name 15%) and its reason is shown on the review page. New column `document_metadata.folder_reason` (added automatically to older databases).
- OCR without Tesseract: when OpenAI is on and Tesseract isn't installed, photos and scanned PDF pages (up to 10 per PDF) are read by GPT vision (`services/ai/vision.py`, extraction method `OPENAI_VISION`). `/health` reports `ocr_provider`; Settings → AI & Privacy shows it.
- SMTP over SSL (port 465, `SMTP_USE_SSL`, on by default for 465) besides STARTTLS (587); emails get a proper `Message-ID` and `Date`. `flask --app run.py send-test-email <address>` checks the settings.
- 16 new backend tests (115 in total).

### Changed
- Verification codes are only sent by email. Without an email server sign-up and sign-in fail with `503 EMAIL_NOT_SET_UP`; showing the code on screen needs `EMAIL_DEMO_MODE=true` and has no effect once `SMTP_HOST` is set.

### Fixed
- `flask init-db` could not create a missing MySQL database (`url.set(database=None)` kept the database name).
- GPT could pick a folder about a different subject in the same semester (e.g. a Networks lab into Database Systems).

## [0.2.0] — 2026-11-17

Changes asked for after the demonstration (product review + teacher's comments).

### Added — backend

- Two-step verification by email code (OTP): `POST /auth/register` emails a code and the account is created by `POST /auth/register/verify` (which also signs the user in); `POST /auth/login` emails a code that is checked by `POST /auth/login/verify`; `POST /auth/resend-code`. Codes are 6 digits, stored hashed, expire after 10 minutes and stop working after 5 wrong tries. SMTP settings in `.env`; without them the API runs in demo mode and returns the code. `TWO_FACTOR_ENABLED` switches it off.
- AI folder recommendation (`services/recommend.py`): `GET /documents/{id}/analysis` returns `folder_recommendations` — the user's existing folders ranked by similar documents, folder-name match and the AI's own path, each with a reason; a new folder is only suggested when nothing fits.
- Folder rename (`PATCH /folders/{id}`), delete (`DELETE /folders/{id}`, documents go to the Recycle bin) and AI summary of a folder and its subfolders (`GET /folders/{id}/summary`, offline or OpenAI)
- Recycle bin: `POST /documents/{id}/trash`, `POST /documents/{id}/restore` (re-creates the original folder), `GET /trash`, `DELETE /trash`; new file status `DELETED` and columns `files.deleted_at`, `files.deleted_from_path`
- AI search also returns matching `folders` (by folder name and by where the best results are)
- `sort=updated_at` for `GET /documents`; `in_recycle_bin` in dashboard stats; `two_factor_enabled` / `email_configured` in `/health`
- Automatic database upgrade (`app/upgrade.py`): older databases get the new columns and status on the first request or with `flask init-db` — no data is lost
- 19 new backend tests (99 in total)

### Added — frontend

- Sign-in and sign-up code step (`VerificationCodeStep`), resend with countdown, demo-mode banner
- OneDrive-style sidebar with "+ Create or upload", **Home**, **My files**, **Recycle bin**
- **My files** explorer (`/files`): breadcrumb, folders and files together, list or tiles view, filter by name, sort, ⋯ menu (open, download, rename, delete, summarise), new folder
- **Home**: AI search box, **Your folders** tiles with "AI summary", **Recent files** list with filter and actions
- **Recycle bin** page (`/recycle-bin`): restore, delete for good, empty bin
- Review page: **AI suggested folder** card (best existing folder pre-selected); upload page shows the suggested folder
- AI Search shows matching **folders** with an Open button
- 8 new frontend tests (93 in total)

### Changed

- Deleting a document from the app now moves it to the Recycle bin (discarding an upload in review still deletes it at once)
- The old "All Folders" page is replaced by My files (`/folders` links redirect)

## [0.1.0] — 2026-10-30

First working version of the application.

### Added — backend (Flask)

- Registration and login with FR-01 password rules, BCrypt hashing, JWT (30 min), lockout after 5 failed logins
- Upload of PDF, DOCX, TXT, PNG and JPG with content-type check, size limit, integrity check and storage quota
- Exact duplicate detection (SHA-256, per user) with "upload anyway" option
- Background processing pipeline: PyMuPDF, python-docx, Tesseract OCR (optional) and plain-text extraction; scanned-PDF OCR fallback; automatic recovery of interrupted jobs
- Offline AI analyser: category, document type, title, summary, keywords, filename and folder suggestions (reuses the user's existing folders)
- Optional OpenAI GPT analysis with output validation and automatic fallback; optional OpenAI or Sentence-Transformers embeddings
- Similar-document detection using embeddings
- Natural-language search (semantic + keyword ranking) with a per-user in-memory index
- Review and approve flow, edit / rename / move, folders, categories, dashboard statistics, profile and password change
- Local or AWS S3 file storage with short-lived signed download links
- Audit log for logins, uploads, approvals, views, downloads, edits, deletes and searches
- CLI commands: `init-db`, `seed-demo` (demo account with 9 sample documents), `reindex`
- 80 automated backend tests (86% coverage)

### Added — frontend (React)

- Login, registration with live password checklist, dashboard, upload with drag-and-drop and progress, AI review page, review queue, natural-language search, documents list, document details with preview, folders, categories, profile and settings
- Responsive layout with off-canvas sidebar on phones; automatic sign-out when the session expires
- 85 automated tests (Vitest + React Testing Library)

### Added — tooling

- `setup.bat` (one-time Windows setup) and `start-dev.bat` (starts both servers and opens the browser)

### Changed — documentation

- API specification updated to the implemented v1.0 endpoints
- Architecture: AI providers, search design and technical decisions recorded
- Database design: duplicate columns on `document_metadata`, keyword order, `FULLTEXT` index removed
- Testing strategy: test results, AI evaluation and measured response times

## [0.0.1] — 2026-10-30

### Added

- Repository structure (`docs/`, `frontend/`, `backend/`, `database/`)
- Project documentation set based on the NIT3003 proposal and presentation
- MySQL schema `database/schema.sql`
- `.gitignore`, `.gitattributes`, pull request template, contributing guide

## Milestones

- **M2 — Oral presentation** (NIT3003): completed
- **M1 — Project proposal** (NIT3003): completed
