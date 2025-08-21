function readJSON(id) {
    const el = document.getElementById(id);
    try { return JSON.parse(el.textContent || ""); } catch { return ""; }
}

// Render Markdown into each panel
document.getElementById('skill-gap-rendered').innerHTML = marked.parse(readJSON('data-skill-gap') || "");
document.getElementById('project-ideas-rendered').innerHTML = marked.parse(readJSON('data-project-ideas') || "");
document.getElementById('improvement-areas-rendered').innerHTML = marked.parse(readJSON('data-improvement-areas') || "");

