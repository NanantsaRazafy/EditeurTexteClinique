// testApi.js
const http = require('http');

// Mot à tester
const wordToTest = "fiainano";

// Données envoyées au endpoint /analyze
const postData = JSON.stringify({
  text: wordToTest,
  lang: "mg"
});

const options = {
  hostname: 'localhost',  // ton FastAPI tourne ici
  port: 8000,             // port de ton FastAPI
  path: '/analyze',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(postData)
  }
};

// Requête HTTP POST vers /analyze
const req = http.request(options, (res) => {
  let data = '';

  res.on('data', chunk => {
    data += chunk;
  });

  res.on('end', () => {
    try {
      const json = JSON.parse(data);
      
      // Vérifie si le pipeline fournit un champ corrected_text
      const corrected = json.corrected_text || wordToTest;
      
      console.log('Texte original :', wordToTest);
      console.log('Texte corrigé :', corrected);
      console.log('Analyse complète :', JSON.stringify(json, null, 2));
    } catch (err) {
      console.error('Erreur parsing JSON:', err);
      console.log('Réponse brute :', data);
    }
  });
});

req.on('error', (err) => {
  console.error('Erreur requête HTTP :', err);
});

req.write(postData);
req.end();
