"""Development entry point.

    flask --app run.py init-db      # create tables
    flask --app run.py seed-demo    # optional demo account with sample documents
    flask --app run.py run --port 5000
"""
import sys

from settings_files import load_settings

settings_files = load_settings()  # backend/.env (see settings_files.py), before the app reads its config

from app import create_app  # noqa: E402
from app.startup import print_report  # noqa: E402

app = create_app()

# When the server starts (`flask run` or `python run.py`), print what is set up and what is missing.
if __name__ == "__main__" or "run" in sys.argv[1:]:
    print_report(app, settings_files)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
