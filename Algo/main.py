from fastapi import FastAPI
from pydantic import BaseModel
from NLP.pipeline import analyze as nlp_analyze
from pathlib import Path
from NLP.translate import load_dictionary_csv, lookup

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parents[1]  
DICT_PATH = BASE_DIR / "Data" / "dict_mg_fr.csv"
DICT_MG_FR = load_dictionary_csv(DICT_PATH)


class AnalyzeRequest(BaseModel):
    text: str
    lang: str = "fr"

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    # TODO: 
    return nlp_analyze(req.text, req.lang)

@app.get("/translate")
def translate(word: str, src: str = "mg", dst: str = "fr"):
    # pour l'instant on supporte mg->fr uniquement (simple)
    if src != "mg" or dst != "fr":
        return {"error": "Only mg->fr supported for now", "src": src, "dst": dst}

    return lookup(word, DICT_MG_FR)
