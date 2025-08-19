window.onload = function() {
    sortJobs(); // page load hote hi default sorting apply ho jaaye
};

function sortJobs() {
    const sortBy = document.getElementById("sortBy").value;
    const container = document.getElementById("jobCards");
    const cards = Array.from(container.getElementsByClassName("job-card"));

    cards.sort((a, b) => {
    if (sortBy === "applicantsCount") {
        return parseInt(a.dataset.applicants) - parseInt(b.dataset.applicants); // ascending
    } else if (sortBy === "postedAt") {
        return new Date(b.dataset.posted) - new Date(a.dataset.posted); // newest first
    }
});

    // Re-append in sorted order
    cards.forEach(card => container.appendChild(card));
}
