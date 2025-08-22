document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.accordion-button').forEach(button => {
        button.addEventListener('click', function () {
            const collapseElement = document.querySelector(this.dataset.bsTarget);
            const bsCollapse = bootstrap.Collapse.getOrCreateInstance(collapseElement);
            if (collapseElement.classList.contains('show')) {
                bsCollapse.hide();
            } else {
                bsCollapse.show();
            }
        });
    });
});


function readJSON(id) {
    const el = document.getElementById(id);
    try { return JSON.parse(el.textContent || ""); } catch { return ""; }
}

// Render Markdown into each panel
document.getElementById('skill-gap-rendered').innerHTML = marked.parse(readJSON('data-skill-gap') || "");
document.getElementById('project-ideas-rendered').innerHTML = marked.parse(readJSON('data-project-ideas') || "");
document.getElementById('improvement-areas-rendered').innerHTML = marked.parse(readJSON('data-improvement-areas') || "");


