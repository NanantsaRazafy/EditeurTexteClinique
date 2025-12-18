import requests
from bs4 import BeautifulSoup

url = "https://nybaiboly.net/Bible.htm"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.text, "html.parser")

# ⚠️ PAS mw-parser-output
content = soup.find("div", id="content") or soup.find("div", class_="content")

text = ""

if content:
    text = content.get_text(separator="\n", strip=True)

with open("../raw/baiboly_raw2.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("✔ Texte récupéré :", len(text), "caractères")
