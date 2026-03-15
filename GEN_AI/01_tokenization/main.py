import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey There! My Name is Abhi"

tokens = enc.encode(text)

deconded_text = enc.decode(tokens=tokens)

print("Tokens",tokens)
print(f"Decoded Tokens: {deconded_text}")