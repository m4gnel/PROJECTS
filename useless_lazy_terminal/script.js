const runBtn = document.getElementById("run-btn");
const debugBtn = document.getElementById("debug-btn");
const clearBtn = document.getElementById("clear-btn");
const editor = document.getElementById("editor");
const output = document.getElementById("output");
const mainContent = document.querySelector(".main");
const terminal = document.getElementById("terminal");
const resizer = document.getElementById("resizer");
const sidebar = document.getElementById("sidebar");

const openFileInput = document.getElementById("open-file-input");

const lazyResponses = [
  "Ugh, do I really have to?",
  "Can't we just chill instead?",
  "Maybe tomorrow... or next week.",
  "I’m so tired... let's pretend it worked.",
  "Meh, close enough.",
  "Running code? How about a nap instead?",
  "I’d debug it, but I’m too lazy right now.",
  "I'll get to it... eventually.",
  "This looks fine. Probably.",
  "Let's just say it works and move on.",
  "Honestly, who even reads these errors?",
  "I’m not your debugger, buddy.",
  "If it breaks, blame the compiler.",
  "Running your code... but don’t expect miracles.",
  "Why write code when we can just imagine it?",
];

function getRandomLazyResponse() {
  const idx = Math.floor(Math.random() * lazyResponses.length);
  return lazyResponses[idx];
}

function appendPrompt() {
  const promptLine = document.createElement("div");
  promptLine.innerHTML = `<span class="prompt">C:\\Users\\User\\bash></span><input type="text" class="terminal-input" autocomplete="off" />`;
  output.appendChild(promptLine);
  output.scrollTop = output.scrollHeight;
  promptLine.querySelector("input").focus();
}

output.addEventListener("keydown", function (e) {
  if (e.target.classList.contains("terminal-input") && e.key === "Enter") {
    e.preventDefault();
    const inputValue = e.target.value.trim();
    if (!inputValue) return;

    e.target.disabled = true;
    e.target.style.color = "#2196f3";
    e.target.style.background = "transparent";
    e.target.style.border = "none";
    e.target.style.outline = "none";
    e.target.style.caretColor = "transparent";
    e.target.style.pointerEvents = "none";

    const responseDiv = document.createElement("div");
    responseDiv.style.color = "red";
    responseDiv.innerText = getRandomLazyResponse();
    output.appendChild(responseDiv);

    appendPrompt();

    output.scrollTop = output.scrollHeight;
  }
});

runBtn.addEventListener("click", () => {
  const code = editor.innerText.trim();
  const currentLang = document.getElementById("tab-name").textContent;

  const codeBlock = document.createElement("div");
  codeBlock.style.color = "#ccc";
  codeBlock.style.marginBottom = "8px";
  codeBlock.style.fontFamily = "monospace";
  codeBlock.style.whiteSpace = "pre-wrap";
  codeBlock.innerText = code || `// No ${currentLang} code written.`;
  output.appendChild(codeBlock);

  const runOutput = `Running your ${currentLang} program...`;
  const result = document.createElement("div");
  result.style.color = "#00ff00";
  result.innerText = runOutput;
  output.appendChild(result);

  const lazyRunReply = document.createElement("div");
  lazyRunReply.style.color = "red";
  lazyRunReply.innerText = getRandomLazyResponse();
  output.appendChild(lazyRunReply);

  appendPrompt();

  output.scrollTop = output.scrollHeight;
});

debugBtn.addEventListener("click", () => {
  const lazyMessage = "Debugging... ugh, I'm lazy, but okay.";
  const lazyEl = document.createElement("div");
  lazyEl.style.color = "red";
  lazyEl.innerText = lazyMessage;
  output.appendChild(lazyEl);
  appendPrompt();
  output.scrollTop = output.scrollHeight;
});

// ✅ CLEAR BUTTON FUNCTIONALITY
clearBtn.addEventListener("click", () => {
  editor.innerText = "";
});

document.querySelectorAll(".folder").forEach(folder => {
  folder.addEventListener("click", () => {
    const name = folder.dataset.folder;
    document.getElementById("tab-name").textContent = name;
    editor.innerHTML = `// Write your ${name} code here`;
  });
});

// Terminal resize handling
let isResizing = false;
let startY = 0;
let startTerminalHeight = 0;
let startMainHeight = 0;

resizer.addEventListener("mousedown", (e) => {
  isResizing = true;
  startY = e.clientY;
  startTerminalHeight = terminal.offsetHeight;
  startMainHeight = mainContent.offsetHeight;

  document.body.style.userSelect = "none";
});

window.addEventListener("mousemove", (e) => {
  if (!isResizing) return;

  const dy = startY - e.clientY;
  let newTerminalHeight = startTerminalHeight + dy;
  let newMainHeight = startMainHeight - dy;

  const minTerminalHeight = 100;
  const maxTerminalHeight = window.innerHeight - 150;

  if (newTerminalHeight < minTerminalHeight) {
    newTerminalHeight = minTerminalHeight;
    newMainHeight = window.innerHeight - newTerminalHeight - resizer.offsetHeight - document.querySelector('.top-bar').offsetHeight;
  }
  if (newTerminalHeight > maxTerminalHeight) {
    newTerminalHeight = maxTerminalHeight;
    newMainHeight = window.innerHeight - newTerminalHeight - resizer.offsetHeight - document.querySelector('.top-bar').offsetHeight;
  }

  terminal.style.height = newTerminalHeight + "px";
  mainContent.style.height = newMainHeight + "px";
});

window.addEventListener("mouseup", () => {
  if (isResizing) {
    isResizing = false;
    document.body.style.userSelect = "auto";
  }
});

appendPrompt();

// File Menu Features
function downloadFile(filename, content) {
  const blob = new Blob([content], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();
  URL.revokeObjectURL(a.href);
}

document.getElementById("new-file").addEventListener("click", () => {
  if (confirm("Are you sure you want to create a new file? Unsaved changes will be lost.")) {
    editor.innerHTML = "";
    document.getElementById("tab-name").textContent = "Untitled";
  }
});

openFileInput.addEventListener("change", () => {
  const file = openFileInput.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function (e) {
    editor.innerText = e.target.result;
    document.getElementById("tab-name").textContent = file.name;
  };
  reader.readAsText(file);
  openFileInput.value = "";
});

document.getElementById("save-file").addEventListener("click", () => {
  let filename = document.getElementById("tab-name").textContent;
  if (["Untitled", "BASH", "HTML", "CSS", "JS", "JAVA", "PYTHON", "C++", "C", "SQL"].includes(filename)) {
    filename = "code.txt";
  }
  downloadFile(filename, editor.innerText);
});

document.getElementById("save-as-file").addEventListener("click", () => {
  const filename = prompt("Enter file name to save as:", "code.txt");
  if (filename) {
    downloadFile(filename, editor.innerText);
    document.getElementById("tab-name").textContent = filename;
  }
});

// Edit Menu
document.getElementById("undo").addEventListener("click", () => {
  document.execCommand('undo');
});
document.getElementById("redo").addEventListener("click", () => {
  document.execCommand('redo');
});
document.getElementById("cut").addEventListener("click", () => {
  document.execCommand('cut');
});
document.getElementById("copy").addEventListener("click", () => {
  document.execCommand('copy');
});
document.getElementById("paste").addEventListener("click", () => {
  document.execCommand('paste');
});

// View Menu
document.getElementById("toggle-explorer").addEventListener("click", () => {
  if (sidebar.style.display === "none") {
    sidebar.style.display = "block";
    resizer.style.marginLeft = "225px";
    terminal.style.marginLeft = "225px";
    terminal.style.width = "calc(100% - 200px)";
  } else {
    sidebar.style.display = "none";
    resizer.style.marginLeft = "0";
    terminal.style.marginLeft = "0";
    terminal.style.width = "100%";
  }
});

document.getElementById("toggle-terminal").addEventListener("click", () => {
  if (terminal.style.display === "none") {
    terminal.style.display = "flex";
    resizer.style.display = "block";
    mainContent.style.height = `calc(100vh - ${terminal.offsetHeight + resizer.offsetHeight + document.querySelector('.top-bar').offsetHeight}px)`;
  } else {
    terminal.style.display = "none";
    resizer.style.display = "none";
    mainContent.style.height = `calc(100vh - ${document.querySelector('.top-bar').offsetHeight}px)`;
  }
});

document.getElementById("toggle-extensions").addEventListener("click", () => {
  alert("Extensions panel not implemented yet.");
});

// Terminal Menu
document.getElementById("new-terminal").addEventListener("click", () => {
  output.innerHTML = `Microsoft Windows [Version 10.0.19045.4046]<br>(c) Microsoft Corporation. All rights reserved.<br><br>`;
  appendPrompt();
});

document.getElementById("split-terminal").addEventListener("click", () => {
  alert("Split Terminal feature not implemented yet.");
});

// Run Menu
document.getElementById("start-debugging").addEventListener("click", () => {
  debugBtn.click();
});
document.getElementById("run-without-debugging").addEventListener("click", () => {
  runBtn.click();
});
