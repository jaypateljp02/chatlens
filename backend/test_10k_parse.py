from parser.whatsapp_parser import parse_whatsapp_chat

# Generate a 10,000 message WhatsApp test chat
lines = []
for i in range(1, 10001):
    sender = f"User_{i % 5}"
    lines.append(f"[{i%28+1:02d}/01/2026, 10:15:{i%60:02d}] {sender}: Message item number {i} discussing project deliverable {i}.")

chat_text = "\n".join(lines)
msgs, meta = parse_whatsapp_chat(chat_text, "Large_10K_Chat_Export.txt")

print("==========================================")
print(f"PARSED TOTAL MESSAGES: {len(msgs)}")
print(f"METADATA TOTAL MESSAGES: {meta.total_messages}")
print(f"PARTICIPANTS COUNT: {len(meta.participants)}")
print("==========================================")
assert len(msgs) == 10000
print("10,000 MESSAGE PARSING: 100% VERIFIED SUCCESS!")
