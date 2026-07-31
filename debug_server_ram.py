import sys
sys.path.append('backend')
from main import _get_all_stored_messages, _load_session_from_disk, chat_store, STORAGE_DIR, os

print("STORAGE_DIR contents:", os.listdir(STORAGE_DIR))

# Force reload all disk sessions into RAM
for fname in os.listdir(STORAGE_DIR):
    if fname.endswith(".json"):
        cid = fname.replace(".json", "")
        _load_session_from_disk(cid)

print("RAM chat_store keys:", list(chat_store.keys()))
all_msgs = _get_all_stored_messages()
print("TOTAL MASTER MESSAGES COMBINED:", len(all_msgs))

senders = set(m.sender for m in all_msgs if m.sender)
print("TOTAL MASTER SENDERS:", len(senders), list(senders)[:10])
