from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from NLP.pipeline import analyze as nlp_analyze
from pathlib import Path
from NLP.translate import load_dictionary_csv, lookup

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return nlp_analyze(req.text, req.lang)

@app.get("/translate")
def translate(word: str, src: str = "mg", dst: str = "fr"):
    if src != "mg" or dst != "fr":
        return {"error": "Only mg->fr supported"}
    return lookup(word, DICT_MG_FR)
