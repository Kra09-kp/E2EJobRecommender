document.addEventListener("DOMContentLoaded", function () {
    console.log("jobs_script loaded"); // check in console

    // Modal open logic
    document.addEventListener("click", function (e) {
        if (e.target.classList.contains("view-desc-btn")) {
            const jobCard = e.target.closest(".job-card");
            const jobTitle = jobCard.querySelector(".card-title").textContent;
            const jobDescription = jobCard.getAttribute("descriptionHtml") || "No description available.";

            // fill modal
            document.querySelector("#jobDescModal .modal-title").textContent = jobTitle;
            const safeDescription = DOMPurify.sanitize(jobDescription);
            document.getElementById("jobDescContent").innerHTML = safeDescription;

            // open modal
            const modal = new bootstrap.Modal(document.getElementById("jobDescModal"));
            modal.show();
        }
    });

    // toggleSort(); // Initial sort state
});

let originalOrder = [];

// Save initial order once page loads
window.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll("#jobCards .job-card");
    originalOrder = Array.from(cards);
});

function toggleSort() {
    const toggle = document.getElementById("sortToggle");
    const container = document.getElementById("jobCards");

    if (toggle.checked) {
        // Sort by posted date (latest first)
        let cards = Array.from(container.getElementsByClassName("job-card"));
        cards.sort((a, b) => {
            let dateA = new Date(a.dataset.posted.replace(" ", "T"));
            let dateB = new Date(b.dataset.posted.replace(" ", "T"));
            return dateB - dateA; // latest first
        });
        cards.forEach(card => container.appendChild(card));
    } else {
        // Reset to original order
        originalOrder.forEach(card => container.appendChild(card));
    }
}

function loadOtherPlatform(platform) {
  // current query params le lo
  const currentParams = new URLSearchParams(window.location.search);

  // keywords aur location extract
  const keywords = currentParams.get("keywords");
  const location = currentParams.get("location");

  // naye platform ke liye URL banao
  const newUrl = `/job-recommendation/${platform}?keywords=${encodeURIComponent(keywords)}&location=${encodeURIComponent(location)}&fromHome=false`;

  // redirect
  window.location.href = newUrl;
}

const urlParams = new URLSearchParams(window.location.search);
console.log(!urlParams.get("fromHome"))
if (urlParams.get("fromHome") !== "true") {
    document.getElementById("anotherPlatformBtn").style.display = "none";
}
