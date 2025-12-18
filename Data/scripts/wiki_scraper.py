import requests
from bs4 import BeautifulSoup

url = "https://mg.wikipedia.org/wiki/Malagasy"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

content = soup.find("div", class_="mw-parser-output")

text = ""

if content:
    for p in content.find_all("p"):
        text += p.text.strip() + "\n"

with open("../raw/wiki_raw.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("✔ Texte récupéré :", len(text), "caractères")
