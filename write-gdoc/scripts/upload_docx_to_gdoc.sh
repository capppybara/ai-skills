#!/usr/bin/env bash
# Wrapper: run upload_docx_to_gdoc.py under a Python that has the
# google-api-python-client libraries installed. Forwards all args to the
# Python script.
#
# Override the interpreter by exporting GDOC_UPLOAD_PYTHON, e.g.:
#   export GDOC_UPLOAD_PYTHON=$HOME/.venvs/gdoc-upload/bin/python
set -euo pipefail

PY="${GDOC_UPLOAD_PYTHON:-python3}"

if ! command -v "$PY" >/dev/null 2>&1; then
    echo "ERROR: Python interpreter '$PY' not found." >&2
    echo "Install Python 3 or set GDOC_UPLOAD_PYTHON to a valid interpreter." >&2
    exit 2
fi

if ! "$PY" -c "import googleapiclient, google_auth_oauthlib" >/dev/null 2>&1; then
    echo "ERROR: Required Google API libraries not installed in '$PY'." >&2
    echo "Install with:" >&2
    echo "  $PY -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib" >&2
    exit 2
fi

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
exec "$PY" "$SCRIPT_DIR/upload_docx_to_gdoc.py" "$@"
