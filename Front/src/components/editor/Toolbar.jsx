import React from "react";
import { formatText } from "../utils/textActions";

export default function Toolbar({ onSave }) {
  return (
    <div className="toolbar">
      <button className="btn-modern" onClick={() => formatText("bold")}>B</button>
      <button className="btn-modern" onClick={() => formatText("italic")}>I</button>
      <button className="btn-modern" onClick={() => formatText("underline")}>U</button>

      <button className="btn-modern" onClick={() => formatText("justifyLeft")}>Gauche</button>
      <button className="btn-modern" onClick={() => formatText("justifyCenter")}>Centre</button>
      <button className="btn-modern" onClick={() => formatText("justifyRight")}>Droite</button>

      <button className="btn-modern save" onClick={onSave}>
        Sauvegarder
      </button>
    </div>
  );
}
