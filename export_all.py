import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

# --- CONFIGURATION ---
# Replace with your own service account key path
SERVICE_ACCOUNT_FILE = "service-account-key.json" 
# The collection you want to export
TARGET_COLLECTION = "users" 
# Output file name
OUTPUT_FILE = "firestore_backup.json"
# ---------------------

def initialize_firebase():
    """Initializes Firebase Admin SDK safely."""
    if not firebase_admin._apps:
        if not os.path.exists(SERVICE_ACCOUNT_FILE):
            raise FileNotFoundError(f"Key file not found at: {SERVICE_ACCOUNT_FILE}")
            
        cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
        firebase_admin.initialize_app(cred)
        print("🚀 Firebase Admin SDK initialized successfully.")
    return firestore.client()

def fetch_recursive_data(doc_ref):
    """Recursively fetches document data and all its nested sub-collections."""
    # Get current document data
    doc_snapshot = doc_ref.get()
    data = doc_snapshot.to_dict() or {}
    
    # Discover and fetch all sub-collections
    sub_collections = doc_ref.collections()
    for sub_coll in sub_collections:
        print(f"   ∟ Found sub-collection: '{sub_coll.id}' under doc: '{doc_ref.id}'")
        sub_docs_data = {}
        
        # We use stream() here for the sub-documents
        for sub_doc in sub_coll.stream():
            # Recursive call to handle deeper nesting if necessary
            sub_docs_data[sub_doc.id] = fetch_recursive_data(sub_doc.reference)
        
        data[sub_coll.id] = sub_docs_data
        
    return data

def main():
    try:
        db = initialize_firebase()
        print(f"🔍 Scanning for collection: '{TARGET_COLLECTION}'...")
        
        export_data = {TARGET_COLLECTION: {}}
        
        # Use list_documents() to catch "virtual/empty" parent documents
        collection_ref = db.collection(TARGET_COLLECTION)
        docs = list(collection_ref.list_documents())
        
        if not docs:
            print(f"⚠️ No documents found in '{TARGET_COLLECTION}'. Check your collection name.")
            return

        for doc_ref in docs:
            print(f"📄 Processing document: {doc_ref.id}")
            export_data[TARGET_COLLECTION][doc_ref.id] = fetch_recursive_data(doc_ref)

        # Write to JSON file
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=4, default=str, ensure_ascii=False)
        
        print(f"\n✅ Export complete! Data saved to: {OUTPUT_FILE}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
