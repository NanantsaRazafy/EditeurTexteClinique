import React, { useRef, useState, useEffect } from "react";

export default function EditorArea({
  setContent,
  onLinesChange,
  onScroll,
}) {
  const editorRef = useRef(null);
  const [isEmpty, setIsEmpty] = useState(true);

  useEffect(() => {
    editorRef.current.innerHTML = "<div><br></div>";
    onLinesChange(1);
  }, [onLinesChange]);

  const handleInput = () => {
    const text = editorRef.current.innerText;
    setContent(text);
    setIsEmpty(text.trim().length === 0);

    const lines =
      editorRef.current.querySelectorAll("div").length || 1;
    onLinesChange(lines);
  };

  return (
    <div className="editor-container-inner">
      {isEmpty && (
        <div className="editor-placeholder">
          Commencez à écrire ici...
        </div>
      )}

      <div
        ref={editorRef}
        className="editor"
        contentEditable
        onInput={handleInput}
        onScroll={(e) => onScroll(e.target.scrollTop)}
        suppressContentEditableWarning
      ></div>
    </div>
  );
}
