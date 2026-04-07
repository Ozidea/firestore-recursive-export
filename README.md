# Firestore Recursive Export Tool

A robust Python utility designed to export Google Cloud Firestore collections into a structured JSON format. Unlike standard export methods, this tool performs a deep recursive traversal to capture nested sub-collections and "virtual documents."

## 🚀 Why This Tool?
Standard Firestore SDK methods like `.stream()` often fail to retrieve **"Virtual Documents"**—documents that appear in the Firebase Console (usually in italics) because they contain sub-collections but have no fields of their own. 

This utility uses `list_documents()` and a recursive algorithm to ensure that:
1. Every document is captured, even if it has no direct fields.
2. All nested sub-collections at any depth are included in the final output.

## ✨ Features
- **Deep Recursion:** Automatically detects and exports all levels of sub-collections.
- **Virtual Document Support:** Captures documents that exist only as paths for nested data.
- **Clean JSON Output:** Generates a single, well-structured JSON file ready for backup or migration.
- **Environment Aware:** Safe for use in both local scripts and Jupyter/Google Colab notebooks.

## 🛠 Prerequisites
- **Python 3.x**
- **Firebase Admin SDK:** `pip install firebase-admin`
- **Service Account Key:** A `.json` credentials file from the Firebase Console (Project Settings > Service Accounts).

## 📦 Installation
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/firestore-recursive-export.git](https://github.com/YOUR_USERNAME/firestore-recursive-export.git)
   cd firestore-recursive-export
