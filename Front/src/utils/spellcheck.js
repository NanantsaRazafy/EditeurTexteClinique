// ========================================
// DICTIONNAIRE MALAGASY ENRICHI
// ========================================

// Mots courants et particules
const validWords = [
  // Particules et mots grammaticaux
  'amin', 'dia', 'sy', 'ny', 'io', 'ity', 'ireo', 'izay', 'fa',
  'tsy', 'aza', 'koa', 'ihany', 'foana', 'izy', 'aho', 'ianao',
  'isika', 'izahay', 'ianareo', 'izy', 'ireo', 'izao', 'izany',
  'ary', 'ka', 'na', 'satria', 'raha', 'nefa', 'kanefa', 'saingy',
  
  // Verbes d'action courants
  'manoratra', 'mamaky', 'manao', 'misy', 'mba', 'mahazo',
  'mahafantatra', 'manome', 'mandray', 'mandeha', 'mipetraka',
  'mihinana', 'misotro', 'mihevitra', 'miteny', 'mijery',
  'mianatra', 'mampianatra', 'miasa', 'milalao', 'mihira',
  'manompo', 'matory', 'mifoha', 'misasa', 'mianatra',
  'mangataka', 'manontany', 'mamaly', 'mandidy', 'manampy',
  'mitomany', 'mipetraka', 'mitsangana', 'mihomehy', 'manaranaka',
  
  // Noms communs
  'teny', 'soratra', 'olona', 'tanana', 'trano', 'fiainana',
  'fiarahamonina', 'fianarana', 'asa', 'vola', 'sakafo',
  'rano', 'vary', 'kitay', 'afo', 'alina', 'maraina',
  'anio', 'hariva', 'masoandro', 'volana', 'kintana',
  'lanitra', 'tany', 'ranomasina', 'tendrombohitra', 'lohasaha',
  'ala', 'hazo', 'voninkazo', 'ravina', 'voly',
  
  // Adjectifs et descriptions
  'tsara', 'ratsy', 'lehibe', 'kely', 'fotsy', 'mainty',
  'maitso', 'mena', 'manga', 'volomavo', 'vaovao', 'taloha',
  'lava', 'fohy', 'mafana', 'mangatsiaka', 'mando', 'maina',
  'be', 'vitsy', 'feno', 'foana', 'mafy', 'malemy',
  'mavesatra', 'maivana', 'haingana', 'miadana', 'lasa', 'ho',
  
  // Prépositions et locatifs
  'eo', 'ao', 'any', 'aty', 'eto', 'eroa', 'etsy',
  'amin', 'amin\'ny', 'ho', 'avy', 'mankany', 'avy',
  
  // Famille et relations
  'razana', 'ray', 'reny', 'zanaka', 'rahalahy', 'anabavy',
  'dadabe', 'nenibe', 'zafikely', 'havana', 'namana',
  'vadiko', 'vadiny', 'vady', 'zoky', 'zandry',
  'fianakaviana', 'mpirahalahy', 'mpianakavy',
  
  // Lieux de Madagascar
  'madagasikara', 'antananarivo', 'antsirabe', 'toamasina',
  'mahajanga', 'fianarantsoa', 'toliara', 'antsiranana',
  'ambositra', 'morondava', 'manakara', 'nosy', 'be',
  
  // Temps et durée
  'omaly', 'androany', 'rahampitso', 'herinandro', 'volana',
  'taona', 'ora', 'minitra', 'segondra', 'andro',
  'alahady', 'alatsinainy', 'talata', 'alarobia', 'alakamisy',
  'zoma', 'asabotsy', 'maraina', 'antoandro', 'hariva',
  
  // Nombres
  'iray', 'roa', 'telo', 'efatra', 'dimy', 'enina',
  'fito', 'valo', 'sivy', 'folo', 'zato', 'arivo',
  
  // Animaux
  'alika', 'saka', 'vorona', 'trondro', 'omby', 'akoho',
  'gisa', 'kisoa', 'ondry', 'zanak\'omby', 'biby',
  
  // Nourriture et boissons
  'mofo', 'henakisoa', 'henaomby', 'henan\'akoho', 'trondro',
  'legioma', 'voankazo', 'ronono', 'dite', 'siramamy',
  'sakay', 'masaka', 'manga', 'mafana', 'mangatsiaka',
  
  // Corps humain
  'loha', 'maso', 'orona', 'vava', 'sofina', 'tanana',
  'tongotra', 'vatana', 'fo', 'kibony', 'volo', 'nify',
  
  // Nature et environnement
  'rivotra', 'orana', 'hafa', 'masoandro', 'volana', 'kintana',
  'rahona', 'varatra', 'kotroka', 'tafio-drivotra',
  
  // Actions et états
  'mangataka', 'manontany', 'mamaly', 'milaza', 'manambara',
  'mandidy', 'manolotra', 'mandray', 'manome', 'mamerina',
  'manokatra', 'manidy', 'mibanjina', 'mitandrina', 'mitsiry',
  
  // Sentiments et émotions
  'faly', 'malahelo', 'tezitra', 'tahotra', 'sahirana',
  'sambatra', 'kivy', 'sosotra', 'malaina', 'somary',
  
  // Concepts abstraits
  'fitiavana', 'fahalalana', 'fahendrena', 'fahamarinana',
  'fahalemena', 'fahasahiana', 'fanahy', 'hevitra', 'saina',
  
  // Vie quotidienne
  'sakafo', 'fisotro', 'fitafiana', 'kiraro', 'satroka',
  'lamba', 'fandriana', 'latabatra', 'seza', 'varavarana',
  'varavarankely', 'venty', 'boky', 'taratasy', 'penina'
];




const forbiddenPatterns = [
  /\bnb/gi,                
  /\bmk/gi,                
  /\bnk/gi,                
  /dt/gi,                  
  /bp/gi,                 
  /sz/gi,                 
  /kh/gi,                 
  /\bng(?![aeioy])/gi,     
  /[qwx]/gi,               
];

// PRÉFIXES ET SUFFIXES MALAGASY


const commonPrefixes = [
  'mi-', 'ma-', 'man-', 'mam-', 'maha-', 'mpan-', 'mpam-', 'mpi-',
  'fi-', 'fan-', 'fam-', 'faha-', 'if-', 'af-', 'anana-',
  'an-', 'am-', 'a-', 'i-', 'ha-', 'ho-', 'tsy-'
];

const commonSuffixes = [
  '-ana', '-ina', '-na', '-ka', '-tra', '-a', '-y', '-ny',
  '-ko', '-nao', '-nay', '-nareo', '-ntsika'
];


// FONCTIONS PRINCIPALES


export const checkWord = (word) => {
  if (!word || word.length < 2) return true;
  
  const cleanWord = word.toLowerCase().trim();
  
  // Vérification directe dans le dictionnaire
  if (validWords.includes(cleanWord)) {
    return true;
  }
  
  // Vérification avec préfixes
  for (const prefix of commonPrefixes) {
    if (cleanWord.startsWith(prefix.replace('-', ''))) {
      const root = cleanWord.slice(prefix.length - 1);
      if (validWords.includes(root) || root.length < 3) {
        return true;
      }
    }
  }
  
  // Vérification avec suffixes
  for (const suffix of commonSuffixes) {
    if (cleanWord.endsWith(suffix.replace('-', ''))) {
      const root = cleanWord.slice(0, -(suffix.length - 1));
      if (validWords.includes(root) || root.length < 3) {
        return true;
      }
    }
  }
  
  return false;
};

export const hasForbiddenPattern = (word) => {
  if (!word) return false;
  return forbiddenPatterns.some(pattern => pattern.test(word));
};

/**
 * Calcule la distance de Levenshtein entre deux mots
 * @param {string} str1 - Premier mot
 * @param {string} str2 - Deuxième mot
 * @returns {number} - Distance de Levenshtein
 */
export const levenshteinDistance = (str1, str2) => {
  const len1 = str1.length;
  const len2 = str2.length;
  const matrix = [];

  if (len1 === 0) return len2;
  if (len2 === 0) return len1;

  // Initialiser la matrice
  for (let i = 0; i <= len1; i++) {
    matrix[i] = [i];
  }

  for (let j = 0; j <= len2; j++) {
    matrix[0][j] = j;
  }

  // Calculer les distances
  for (let i = 1; i <= len1; i++) {
    for (let j = 1; j <= len2; j++) {
      const cost = str1[i - 1] === str2[j - 1] ? 0 : 1;
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1,           // Suppression
        matrix[i][j - 1] + 1,           // Insertion
        matrix[i - 1][j - 1] + cost     // Substitution
      );
    }
  }

  return matrix[len1][len2];
};

/**
 * Génère des suggestions pour corriger un mot mal orthographié
 * @param {string} word - Le mot à corriger
 * @param {number} maxSuggestions - Nombre maximum de suggestions
 * @returns {Array<string>} - Liste des suggestions
 */
export const getSuggestions = (word, maxSuggestions = 5) => {
  if (!word || word.length < 2) return [];
  
  const cleanWord = word.toLowerCase().trim();
  const suggestions = [];
  
  // Calculer la distance pour chaque mot du dictionnaire
  for (const validWord of validWords) {
    const distance = levenshteinDistance(cleanWord, validWord);
    
    // Accepter les mots avec distance <= 2
    if (distance <= 2 && distance > 0) {
      suggestions.push({
        word: validWord,
        distance: distance
      });
    }
  }
  
  // Trier par distance et retourner les meilleurs
  return suggestions
    .sort((a, b) => a.distance - b.distance)
    .slice(0, maxSuggestions)
    .map(s => s.word);
};

/**
 * Analyse un texte complet et retourne les mots valides/invalides
 * @param {string} text - Le texte à analyser
 * @returns {Object} - Objet contenant les listes de mots
 */
export const analyzeText = (text) => {
  if (!text) return { valid: [], invalid: [], forbidden: [] };
  
  // Nettoyer le HTML
  const plainText = text.replace(/<[^>]*>/g, '');
  const words = plainText.split(/\s+/).filter(w => w.length > 0);
  
  const valid = [];
  const invalid = [];
  const forbidden = [];
  
  words.forEach(word => {
    const cleanWord = word.replace(/[.,!?;:]/g, '');
    
    if (cleanWord.length < 2) return;
    
    if (hasForbiddenPattern(cleanWord)) {
      forbidden.push(cleanWord);
    } else if (checkWord(cleanWord)) {
      valid.push(cleanWord);
    } else {
      invalid.push(cleanWord);
    }
  });
  
  return { 
    valid: [...new Set(valid)],      // Enlever les doublons
    invalid: [...new Set(invalid)], 
    forbidden: [...new Set(forbidden)] 
  };
};

/**
 * Lemmatisation simple : extrait la racine d'un mot malagasy
 * @param {string} word - Le mot à lemmatiser
 * @returns {string} - La racine du mot
 */
export const lemmatize = (word) => {
  if (!word || word.length < 3) return word;
  
  const cleanWord = word.toLowerCase().trim();
  
  // Retirer les préfixes
  for (const prefix of commonPrefixes) {
    const prefixClean = prefix.replace('-', '');
    if (cleanWord.startsWith(prefixClean)) {
      const root = cleanWord.slice(prefixClean.length);
      if (root.length >= 2) {
        return root;
      }
    }
  }
  
  // Retirer les suffixes
  for (const suffix of commonSuffixes) {
    const suffixClean = suffix.replace('-', '');
    if (cleanWord.endsWith(suffixClean)) {
      const root = cleanWord.slice(0, -suffixClean.length);
      if (root.length >= 2) {
        return root;
      }
    }
  }
  
  return cleanWord;
};

/**
 * Vérifie si un texte contient des erreurs
 * @param {string} text - Le texte à vérifier
 * @returns {boolean} - true si des erreurs sont détectées
 */
export const hasErrors = (text) => {
  const analysis = analyzeText(text);
  return analysis.invalid.length > 0 || analysis.forbidden.length > 0;
};

/**
 * Compte le nombre total d'erreurs dans un texte
 * @param {string} text - Le texte à analyser
 * @returns {number} - Nombre d'erreurs
 */
export const countErrors = (text) => {
  const analysis = analyzeText(text);
  return analysis.invalid.length + analysis.forbidden.length;
};

// Export par défaut
export default {
  checkWord,
  hasForbiddenPattern,
  getSuggestions,
  analyzeText,
  lemmatize,
  levenshteinDistance,
  hasErrors,
  countErrors
};