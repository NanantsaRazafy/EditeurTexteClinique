from tokenizer import tokenize

text = "Salama daholo, manao ahoana ianao? Amin'ny 2025-12-18."
for t in tokenize(text):
    print(t, "=>", text[t.start:t.end])
