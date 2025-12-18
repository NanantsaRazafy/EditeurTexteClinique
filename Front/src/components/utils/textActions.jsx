export const formatText = (command) => {
  document.execCommand(command, false, null);
};

export const saveText = (content) => {
  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = "document.txt";
  link.click();
};
