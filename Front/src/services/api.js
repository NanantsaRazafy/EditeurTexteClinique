const API_URL = "http://127.0.0.1:8000";

export async function analyzeTextAPI(text, lang = "mg") {
  const response = await fetch(`${API_URL}/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text, lang }),
  });

  if (!response.ok) {
    throw new Error("Erreur analyse API");
  }

  return response.json();
}

export async function translateWordAPI(word) {
  const response = await fetch(
    `${API_URL}/translate?word=${encodeURIComponent(word)}`
  );

  if (!response.ok) {
    throw new Error("Erreur traduction API");
  }

  return response.json();
}
