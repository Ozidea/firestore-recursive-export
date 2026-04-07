# Firestore Recursive Export

Export a Firestore collection (including nested sub-collections) into a single structured JSON file using Python and the Firebase Admin SDK.

This project is designed for cases where you need a lightweight, scriptable backup/export flow without using full Firestore managed export pipelines.

## Table of Contents
- [Overview](#overview)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Setup](#setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Output Format](#output-format)
- [Troubleshooting](#troubleshooting)
- [Security Notes](#security-notes)
- [Known Limitations](#known-limitations)
- [License](#license)

## Overview

The exporter:
- Initializes Firebase Admin with your service account credentials.
- Starts from one target top-level collection.
- Traverses all documents in that collection.
- Recursively fetches sub-collections under each document.
- Writes everything into one JSON file.

Why this is useful:
- `list_documents()` on the root target collection helps include parent/placeholder documents that may not have direct fields.
- The recursive traversal ensures deeper levels are preserved in one output tree.

## How It Works

The main script is [`export_all.py`](/Users/oguzkurtoglu/PycharmProjects/firestore-recursive-export/export_all.py).

Flow:
1. `initialize_firebase()` checks if Firebase is already initialized and creates a Firestore client.
2. `main()` loads the configured target collection and calls `list_documents()` to enumerate document references.
3. For each document, `fetch_recursive_data(doc_ref)`:
   - reads the current document fields,
   - discovers child sub-collections,
   - recursively exports each child document.
4. Final data is saved to the configured output JSON file.

## Project Structure

```text
firestore-recursive-export/
├── export_all.py          # Main export script
├── requirements.txt       # Python dependencies
├── firestore_backup.json  # Example output artifact
├── README.md
└── LICENSE
```

## Requirements

- Python 3.9+ (3.10+ recommended)
- Access to a Firebase project / Firestore database
- A Firebase service account JSON key

Dependency:
- `firebase-admin>=6.5.0`

## Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd firestore-recursive-export
```

2. (Recommended) Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create/download your Firebase service account key from Firebase Console:
   - Project Settings -> Service Accounts -> Generate new private key
   - Save the file in the project folder (or any secure path)

## Configuration

Open [`export_all.py`](/Users/oguzkurtoglu/PycharmProjects/firestore-recursive-export/export_all.py) and update the configuration constants:

```python
SERVICE_ACCOUNT_FILE = "service-account-key.json"
TARGET_COLLECTION = "users"
OUTPUT_FILE = "firestore_backup.json"
```

- `SERVICE_ACCOUNT_FILE`: path to your service account JSON key
- `TARGET_COLLECTION`: top-level Firestore collection to export
- `OUTPUT_FILE`: destination JSON file

## Usage

Run the exporter:

```bash
python3 export_all.py
```

Expected console output includes:
- Firebase initialization confirmation
- Document-by-document processing logs
- Sub-collection discovery logs
- Final success message with output filename

## Output Format

The generated JSON uses this shape:

```json
{
  "<target_collection>": {
    "<doc_id>": {
      "...document_fields": "...",
      "<subcollection_id>": {
        "<sub_doc_id>": {
          "...nested_fields": "...",
          "<deeper_subcollection_id>": {}
        }
      }
    }
  }
}
```

Example (simplified):

```json
{
  "users": {
    "user_123": {
      "name": "Ada",
      "daily_entries": {
        "2026-03-10": {
          "painScore": 3
        }
      }
    }
  }
}
```

## Troubleshooting

### `Key file not found at: ...`
- Verify `SERVICE_ACCOUNT_FILE` points to the correct location.
- Confirm the file exists and is readable.

### `No documents found in '<collection>'`
- Verify `TARGET_COLLECTION` is correct.
- Confirm the collection is not empty.
- Check that your service account has Firestore read access.

### Permission/credential errors from Firebase
- Regenerate service account key if needed.
- Confirm the key belongs to the same Firebase project you expect.
- Validate IAM roles for Firestore access.

### Unicode/serialization concerns
- Export uses `json.dump(..., ensure_ascii=False, default=str)` to preserve unicode and stringify unsupported types.

## Security Notes

- Never commit service account JSON keys to Git.
- Add the key to `.gitignore` (recommended).
- Rotate keys periodically and revoke unused keys in Google Cloud.
- Treat export files as sensitive if they contain personal/user data.

## Known Limitations

- Configuration is currently hardcoded in `export_all.py` (not CLI/env-driven).
- Export starts from one top-level collection at a time.
- Script runs serially and may be slow for very large datasets.
- The output is a custom JSON tree, not Firestore managed export format.
- Root-level enumeration uses `list_documents()` to catch placeholder documents; sub-collection recursion currently reads child docs via `stream()`.

## License

This project is licensed under the MIT License. See [`LICENSE`](/Users/oguzkurtoglu/PycharmProjects/firestore-recursive-export/LICENSE).
