import React, { useState, useRef, useEffect } from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import { analyzeTextAPI } from '../services/api';

import { 
  FileText, 
  Save, 
  Download, 
  Upload, 
  CheckCircle, 
  AlertCircle, 
  Settings,
  Book,
  Lightbulb,
  TrendingUp
} from 'lucide-react';
import { checkWord, hasForbiddenPattern, getSuggestions, analyzeText } from '../utils/spellcheck';

const MalagasyEditor = () => {
  const [content, setContent] = useState('');
  const [statistics, setStatistics] = useState({ words: 0, chars: 0, errors: 0 });
  const [analysis, setAnalysis] = useState({
    valid: [],
    invalid: [],
    forbidden: []
  });
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [currentWord, setCurrentWord] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const quillRef = useRef(null);

  // Configuration de Quill avec plus d'options
  const modules = {
    toolbar: [
      [{ 'header': [1, 2, 3, false] }],
      ['bold', 'italic', 'underline', 'strike'],
      [{ 'color': [] }, { 'background': [] }],
      [{ 'list': 'ordered'}, { 'list': 'bullet' }],
      [{ 'align': [] }],
      ['link'],
      ['clean']
    ],
  };

  const formats = [
    'header',
    'bold', 'italic', 'underline', 'strike',
    'color', 'background',
    'list', 'bullet',
    'align',
    'link'
  ];

  // Gérer les changements de contenu
  const handleChange = (value) => {
    try {
      setContent(value);
      updateStatistics(value);
      performAnalysis(value);
    } catch (err) {
      console.error('Error in handleChange:', err);
    }
  };

  // Calculer les statistiques
  const updateStatistics = (text) => {
    const plainText = text.replace(/<[^>]*>/g, '');
    const words = plainText.trim().split(/\s+/).filter(w => w.length > 0);
    
    let errors = 0;
    try {
      errors = words.filter(word => {
        const clean = word.replace(/[.,!?;:]/g, '');
        if (clean.length <= 2) return false;
        
        try {
          const isValid = checkWord && typeof checkWord === 'function' ? checkWord(clean) : true;
          const hasForbidden = hasForbiddenPattern && typeof hasForbiddenPattern === 'function' ? hasForbiddenPattern(clean) : false;
          return (!isValid || hasForbidden);
        } catch (err) {
          console.error('Error checking word:', err);
          return false;
        }
      }).length;
    } catch (err) {
      console.error('Error in updateStatistics:', err);
      errors = 0;
    }

    setStatistics({
      words: words.length,
      chars: plainText.length,
      errors: errors
    });
  };

  // Analyser le texte complet
const performAnalysis = async (text) => {
  const plainText = text.replace(/<[^>]*>/g, '').trim();
  if (!plainText) {
    setAnalysis({ valid: [], invalid: [], forbidden: [] });
    setSuggestions([]);
    setShowSuggestions(false);
    return;
  }

  try {
    const result = await analyzeTextAPI(plainText, "mg");

    // Séparer mots valides, invalides et interdits
    const safeResult = {
      valid: result?.valid || [],
      invalid: result?.invalid || [],
      forbidden: result?.forbidden || []
    };
    setAnalysis(safeResult);

    // Compter les erreurs
    setStatistics(prev => ({
      ...prev,
      errors: safeResult.invalid.length + safeResult.forbidden.length
    }));

    // Récupérer la première suggestion si le mot est inconnu
    if (result?.issues && result.issues.length > 0) {
      const firstIssue = result.issues[0];
      if (firstIssue?.suggestions && firstIssue.suggestions.length > 0) {
        setCurrentWord(firstIssue.word);
        setSuggestions(firstIssue.suggestions);
        setShowSuggestions(true);
      } else {
        setShowSuggestions(false);
      }
    } else {
      setShowSuggestions(false);
    }

  } catch (error) {
    console.error("Erreur API analyse:", error);
    setAnalysis({ valid: [], invalid: [], forbidden: [] });
    setSuggestions([]);
    setShowSuggestions(false);
  }
};


  // Sauvegarder le contenu
  const handleSave = () => {
    localStorage.setItem('malagasy-editor-content', content);
    localStorage.setItem('malagasy-editor-timestamp', new Date().toISOString());
    
    // Animation de confirmation
    const button = document.querySelector('.save-button');
    if (button) {
      button.classList.add('scale-95');
      setTimeout(() => button.classList.remove('scale-95'), 200);
    }
    
    alert('✅ Texte sauvegardé avec succès !');
  };

  // Exporter en fichier
  const handleExport = () => {
    const plainText = content.replace(/<[^>]*>/g, '');
    const blob = new Blob([plainText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const timestamp = new Date().toISOString().split('T')[0];
    a.download = `texte-malagasy-${timestamp}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Exporter en HTML
  const handleExportHTML = () => {
    const blob = new Blob([content], { type: 'text/html;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const timestamp = new Date().toISOString().split('T')[0];
    a.download = `texte-malagasy-${timestamp}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Importer un fichier
  const handleImport = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setContent(event.target.result);
      };
      reader.readAsText(file);
    }
  };

  // Nouveau document
  const handleNew = () => {
    if (content && window.confirm('Voulez-vous vraiment créer un nouveau document ? Les modifications non sauvegardées seront perdues.')) {
      setContent('');
      localStorage.removeItem('malagasy-editor-content');
    }
  };

  // Charger le contenu sauvegardé au démarrage
  useEffect(() => {
    const saved = localStorage.getItem('malagasy-editor-content');
    if (saved) {
      setContent(saved);
    }
  }, []);

  // Raccourcis clavier
  useEffect(() => {
    const handleKeyDown = (e) => {
      try {
        // Ctrl+S pour sauvegarder
        if (e.ctrlKey && e.key === 's') {
          e.preventDefault();
          handleSave();
        }
        // Ctrl+E pour exporter
        if (e.ctrlKey && e.key === 'e') {
          e.preventDefault();
          handleExport();
        }
        // Ctrl+N pour nouveau
        if (e.ctrlKey && e.key === 'n') {
          e.preventDefault();
          handleNew();
        }
      } catch (err) {
        console.error('Error in keyboard shortcut:', err);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [content]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-lg border-b-4 border-indigo-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4">
          <div className="flex items-center justify-between flex-wrap gap-4">
            {/* Logo et titre */}
            <div className="flex items-center gap-4">
              <div className="bg-gradient-to-br from-indigo-500 to-purple-600 p-3 rounded-xl shadow-lg">
                <FileText className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-xl sm:text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                  Éditeur Malagasy Intelligent
                </h1>
                <p className="text-xs sm:text-sm text-gray-600 flex items-center gap-2">
                  <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                  IA de correction orthographique active
                </p>
              </div>
            </div>
            
            {/* Barre d'outils */}
            <div className="flex items-center gap-2 flex-wrap">
              <button
                onClick={handleNew}
                className="flex items-center gap-2 px-3 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-all shadow-md hover:shadow-lg text-sm"
                title="Nouveau (Ctrl+N)"
              >
                <FileText className="w-4 h-4" />
                <span className="hidden sm:inline">Nouveau</span>
              </button>

              <button
                onClick={handleSave}
                className="save-button flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:from-green-600 hover:to-green-700 transition-all shadow-md hover:shadow-lg text-sm"
                title="Sauvegarder (Ctrl+S)"
              >
                <Save className="w-4 h-4" />
                <span className="hidden sm:inline">Sauvegarder</span>
              </button>
              
              <button
                onClick={handleExport}
                className="flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all shadow-md hover:shadow-lg text-sm"
                title="Exporter (Ctrl+E)"
              >
                <Download className="w-4 h-4" />
                <span className="hidden sm:inline">Exporter</span>
              </button>
              
              <label className="flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-lg hover:from-purple-600 hover:to-purple-700 transition-all shadow-md hover:shadow-lg cursor-pointer text-sm">
                <Upload className="w-4 h-4" />
                <span className="hidden sm:inline">Importer</span>
                <input
                  type="file"
                  accept=".txt,.html"
                  onChange={handleImport}
                  className="hidden"
                />
              </label>

              <button 
                className="p-2 text-gray-600 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition"
                title="Paramètres"
              >
                <Settings className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Contenu principal */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          
          {/* Zone d'édition principale */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
              {/* Barre d'info */}
              <div className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 px-4 sm:px-6 py-3 sm:py-4 text-white">
                <div className="flex items-center justify-between flex-wrap gap-3">
                  <div className="flex items-center gap-3">
                    <CheckCircle className="w-5 h-5" />
                    <span className="text-xs sm:text-sm font-medium">
                      Analyse en temps réel
                    </span>
                  </div>
                  <div className="flex items-center gap-2 sm:gap-4 text-xs sm:text-sm">
                    <span>{statistics.words} mots</span>
                    <span className="hidden sm:inline">•</span>
                    <span className="hidden sm:inline">{statistics.chars} caractères</span>
                    {statistics.errors > 0 && (
                      <>
                        <span className="hidden sm:inline">•</span>
                        <span className="text-yellow-300 flex items-center gap-1">
                          <AlertCircle className="w-4 h-4" />
                          {statistics.errors} erreurs
                        </span>
                      </>
                    )}
                  </div>
                </div>
              </div>

              {/* Éditeur Quill */}
              <div className="p-4 sm:p-6">
                <ReactQuill
                  ref={quillRef}
                  theme="snow"
                  value={content}
                  onChange={handleChange}
                  modules={modules}
                  formats={formats}
                  placeholder="Manoratra eto... Commencez à écrire en Malagasy..."
                  className="min-h-[400px] sm:min-h-[500px]"
                />

                {showSuggestions && suggestions.length > 0 && (
  <div className="mt-2 p-2 bg-yellow-100 text-yellow-800 rounded shadow">
    <strong>Mot suggéré pour "{currentWord}" :</strong> {suggestions[0]}
  </div>
)}

              </div>
            </div>

            {/* Légende et aide */}
            <div className="mt-6 bg-white rounded-xl shadow-md p-4 sm:p-6">
              <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
                <Lightbulb className="w-5 h-5 text-indigo-600" />
                Guide de correction automatique
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 text-sm">
                <div className="flex items-center gap-3 p-3 bg-red-50 rounded-lg">
                  <span className="bg-red-200 text-red-800 px-2 sm:px-3 py-1 rounded font-medium text-xs sm:text-sm">nb</span>
                  <span className="text-gray-700 text-xs sm:text-sm">Pattern interdit (nb, mk, dt, bp, sz)</span>
                </div>
                <div className="flex items-center gap-3 p-3 bg-yellow-50 rounded-lg">
                  <span className="border-b-2 border-yellow-500 px-2 sm:px-3 py-1 font-medium text-xs sm:text-sm">mot</span>
                  <span className="text-gray-700 text-xs sm:text-sm">Erreur orthographique possible</span>
                </div>
                <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
                  <CheckCircle className="w-5 sm:w-6 h-5 sm:h-6 text-green-600" />
                  <span className="text-gray-700 text-xs sm:text-sm">Orthographe correcte validée</span>
                </div>
                <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg">
                  <Book className="w-5 sm:w-6 h-5 sm:h-6 text-blue-600" />
                  <span className="text-gray-700 text-xs sm:text-sm">Dictionnaire Malagasy intégré</span>
                </div>
              </div>
            </div>
          </div>

          {/* Panneau latéral */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl shadow-xl p-4 sm:p-6 sticky top-8">
              <h3 className="font-bold text-base sm:text-lg text-gray-800 mb-4 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-indigo-600" />
                Statistiques
              </h3>
              
              <div className="space-y-3 sm:space-y-4">
                <div className="p-3 sm:p-4 bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl">
                  <div className="text-2xl sm:text-3xl font-bold text-blue-600">{statistics.words}</div>
                  <div className="text-xs sm:text-sm text-gray-600">Mots au total</div>
                </div>

                <div className="p-3 sm:p-4 bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl">
                  <div className="text-2xl sm:text-3xl font-bold text-purple-600">{statistics.chars}</div>
                  <div className="text-xs sm:text-sm text-gray-600">Caractères</div>
                </div>

                <div className="p-3 sm:p-4 bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-xl">
                  <div className="text-2xl sm:text-3xl font-bold text-yellow-600">{statistics.errors}</div>
                  <div className="text-xs sm:text-sm text-gray-600">Erreurs détectées</div>
                </div>

                {statistics.errors > 0 && (
                  <div className="mt-4 p-3 sm:p-4 bg-red-50 rounded-xl border border-red-200">
                    <p className="text-xs sm:text-sm text-red-800 flex items-center gap-2">
                      <AlertCircle className="w-4 h-4" />
                      Corrections recommandées disponibles
                    </p>
                  </div>
                )}

                {statistics.errors === 0 && statistics.words > 0 && (
                  <div className="mt-4 p-3 sm:p-4 bg-green-50 rounded-xl border border-green-200">
                    <p className="text-xs sm:text-sm text-green-800 flex items-center gap-2">
                      <CheckCircle className="w-4 h-4" />
                      Excellent ! Aucune erreur détectée
                    </p>
                  </div>
                )}
              </div>

              <div className="mt-6 pt-6 border-t border-gray-200">
                <h4 className="font-semibold text-xs sm:text-sm text-gray-700 mb-3">Raccourcis clavier</h4>
                <div className="space-y-2 text-xs text-gray-600">
                  <div className="flex justify-between items-center">
                    <span>Sauvegarder</span>
                    <kbd className="px-2 py-1 bg-gray-100 rounded text-xs">Ctrl+S</kbd>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Exporter</span>
                    <kbd className="px-2 py-1 bg-gray-100 rounded text-xs">Ctrl+E</kbd>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Nouveau</span>
                    <kbd className="px-2 py-1 bg-gray-100 rounded text-xs">Ctrl+N</kbd>
                  </div>
                </div>
              </div>

              {/* Informations supplémentaires */}
              <div className="mt-6 pt-6 border-t border-gray-200">
                <h4 className="font-semibold text-xs sm:text-sm text-gray-700 mb-2">Analysé</h4>
                <div className="text-xs text-gray-600 space-y-1">
                  <div className="flex justify-between">
                    <span>Mots valides:</span>
                    <span className="font-medium text-green-600">{analysis.valid.length}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Mots invalides:</span>
                    <span className="font-medium text-yellow-600">{analysis.invalid.length}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Patterns interdits:</span>
                    <span className="font-medium text-red-600">{analysis.forbidden.length}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4">
          <p className="text-center text-xs sm:text-sm text-gray-600">
            Éditeur Malagasy Intelligent - Développé pour Madagascar 🇲🇬
          </p>
        </div>
      </footer>
    </div>
  );
};

export default MalagasyEditor;