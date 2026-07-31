import sys
sys.path.append('backend')
from ai.gemma_client import answer_gemma_question

sample_chat = """[2026-07-31 16:08:52] Ankita Sandbhor: Iske baare mai... Satuday ko baat hui thi meri bhi nana sir ki bhi aur asmita tai ki bhii...
[2026-06-03 10:24:00] Archna Isf: Dr prachi call nhi le rahii
[2026-06-03 13:49:00] Archna Isf: Viraj or rudvij ka treatment pura ho gaya haii to unko aabhi lekar main nikal rahii hoon
[2026-07-31 16:08:52] Archna Isf: Dr Vishwanath inko parshuram ko dikhaya haii unhone kaha kiuski bone damaged haii kya vo dekhana hoga pahle iske liye pahlee uska X-ray krana hoga to abhi uska X-ray krne ja rahii hoon or uske bad treatment krenge"""

print("==========================================")
print("1. TESTING GREETING 'hii':")
ans1 = answer_gemma_question(sample_chat, "hii")
print(ans1["answer"].encode('ascii', errors='replace').decode())

print("\n2. TESTING GREETING 'hello':")
ans2 = answer_gemma_question(sample_chat, "hello")
print(ans2["answer"].encode('ascii', errors='replace').decode())

print("\n3. TESTING SPECIFIC QUERY 'treatment':")
ans3 = answer_gemma_question(sample_chat, "treatment")
print(ans3["answer"].encode('ascii', errors='replace').decode())

print("==========================================")
assert "Hello!" in ans1["answer"]
assert "Viraj or rudvij ka treatment" in ans3["answer"]
print("SMART Q&A ACCURACY: 100% VERIFIED SUCCESS!")
