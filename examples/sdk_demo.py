"""
SDK Demonstration script for Personal Knowledge Graph System.
Requires the backend server running on http://localhost:8000.
"""
import sys
from pathlib import Path

# Add project root to sys.path so knowledge_sdk can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

from knowledge_sdk import ApiClient, Configuration
from knowledge_sdk.api.notes_api import NotesApi
from knowledge_sdk.models.note_create import NoteCreate
from knowledge_sdk.models.link_create import LinkCreate

def main():
    print("Connecting to Personal Knowledge Graph API at http://localhost:8000...")
    config = Configuration(host="http://localhost:8000")
    client = ApiClient(config)
    notes_api = NotesApi(client)

    print("\n1. Listing existing notes...")
    existing = notes_api.list_notes()
    print(f"Found {len(existing)} existing notes.")

    print("\n2. Creating Note Alpha via SDK...")
    note_a = notes_api.create_note(NoteCreate(
        title="SDK Note Alpha",
        content="This note was created automatically via the generated Python SDK.",
        tags=["sdk", "automation"]
    ))
    print(f"Created Note ID: {note_a.id}, Title: '{note_a.title}'")

    print("\n3. Creating Note Beta via SDK...")
    note_b = notes_api.create_note(NoteCreate(
        title="SDK Note Beta",
        content="Target note for SDK link test.",
        tags=["sdk", "testing"]
    ))
    print(f"Created Note ID: {note_b.id}, Title: '{note_b.title}'")

    print(f"\n4. Manually linking Note {note_a.id} -> Note {note_b.id}...")
    link = notes_api.link_notes(note_id=note_a.id, link_create=LinkCreate(target_id=note_b.id))
    print(f"Linked: Source ID {link.source_id} -> Target ID {link.target_id} (Origin: {link.origin})")

    print(f"\n5. Fetching backlinks for Note Beta (ID: {note_b.id})...")
    backlinks = notes_api.get_note_backlinks(note_id=note_b.id)
    print(f"Backlinks count: {len(backlinks)}")
    for b in backlinks:
        print(f" - Backlink from Note ID {b.id}: '{b.title}' (Origin: {b.origin})")

    print("\nSDK Demo completed successfully!")

if __name__ == "__main__":
    main()
