import React, { useState } from "react";
import Toolbar from "./Toolbar";
import EditorArea from "./EditorArea";
import LineNumbers from "./LineNumbers";
import { saveText } from "../utils/textActions";

export default function TextEditor() {
  const [content, setContent] = useState("");
  const [lines, setLines] = useState(1);
  const [scrollTop, setScrollTop] = useState(0);

  return (
    <div className="editor-container">
      <h1> 👻 Ghost Code</h1>

      <Toolbar onSave={() => saveText(content)} />

      <div className="editor-wrapper">
        <LineNumbers lines={lines} scrollTop={scrollTop} />

        <EditorArea
          setContent={setContent}
          onLinesChange={setLines}
          onScroll={setScrollTop}
        />
      </div>
    </div>
  );
}
