# Firestore Recursive Export Tool

A Python-based utility to export Google Cloud Firestore collections, including "virtual documents" and all nested sub-collections, into a structured JSON file.

## Why this tool?
Standard Firestore export tools or SDK methods like `.stream()` often skip "virtual documents"—documents that appear in the Firebase Console (italics) because they have sub-collections but no fields of their own. This script uses `list_documents()` and recursive traversal to ensure every piece of data, including deep-nested sub-collections (like `daily_entries`), is captured.

## Features
- **Deep Export:** Recursively fetches all sub-collections.
- **Virtual Document Support:** Captures documents that only exist as paths for sub-collections.
- **JSON Output:** Saves everything into a single, readable JSON file.
- **Error Handling:** Prevents "App already exists" errors in notebook environments.

## Prerequisites
- Python 3.x
- Firebase Admin SDK
- A Service Account Key (`.json` file) from Firebase Console.

## Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/firestore-recursive-export.git](https://github.com/YOUR_USERNAME/firestore-recursive-export.git)
   cd firestore-recursive-export
