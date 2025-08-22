 // Store keywords for second API call
let extractedKeywords = [];
const SESSION_KEY = "resumeSession";
let sessionId = null;

document.addEventListener("DOMContentLoaded", () => {
  const SESSION_KEY = "resumeSession";
  
  let sessionData = localStorage.getItem(SESSION_KEY);

  if (sessionData) {
    const parsed = JSON.parse(sessionData);
    if (Date.now() < parsed.expiry) {
      sessionId = parsed.sessionId;
      console.log("Valid session found:", sessionId);
    } else {
      localStorage.removeItem(SESSION_KEY);
    }
  }
});


async function uploadResume() {
    const fileInput = document.getElementById("resumeFile");
    const resultDiv = document.getElementById("result");
    const EXPIRY_MS = 6 * 60 * 60 * 1000; // 6 hours


    if (fileInput.files.length === 0) {
        alert("Please select a PDF file first");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

  try {
      if (!sessionId) {
      // Hit your backend endpoint to get a new session id
      const res = await fetch("/create-session", {
        method: "POST"
      });
      const data = await res.json();
      sessionId = data.sessionId;

      // Save it with expiry
      localStorage.setItem(
        SESSION_KEY,
        JSON.stringify({ sessionId, expiry: Date.now() + EXPIRY_MS })
      );

      console.log("New session created:", sessionId);
    }
        
    let response = await fetch("/keywords", {
      method: "POST",
      headers: {
        "X-Session-Id": sessionId
      },
      body: formData
    });

    if (!response.ok) {
      resultDiv.innerHTML = `<span style="color: red;">Error: ${response.statusText}</span>`;
      return;
    }

    const data = await response.json();
    // Update localStorage with file info
    localStorage.setItem(
      SESSION_KEY,
      JSON.stringify({
        sessionId,
        fileName: fileInput.files[0].name,
        expiry: Date.now() + EXPIRY_MS
      })
    );
    
    if (data.keywords) {
      extractedKeywords = data.keywords
      resultDiv.innerHTML = `<strong>Recommended Keywords:</strong> ${data.keywords.join(", ")}`;
      renderButtons();
    } else {
      resultDiv.innerHTML = `<span style="color: yellow;">No keywords found in response.</span>`;
    }
    

  } catch (error) {
    resultDiv.innerHTML = `<span style="color: red;">Error: ${error.message}</span>`;
  }
}

function renderButtons() {
  document.getElementById("nextStep").innerHTML = `
      <input type="text" id="locationInput" placeholder="Enter location" style="padding:6px; border-radius:4px; margin-right:8px;">
      <button type="button" onclick="getLinkedInJobs()" style="padding:8px 14px; border-radius:6px; margin-right:10px; cursor:pointer;">
          Get LinkedIn Jobs
      </button>
      <button type="button" onclick="getNaukriJobs()" style="padding:8px 14px; border-radius:6px; cursor:pointer;">
          Get Naukri Jobs
      </button>
      <button type="button" onclick="getSuggestions()" style="padding:8px 14px; border-radius:6px; cursor:pointer;">
          Get Suggestions
      </button>`;
}

function resetResume() {
  localStorage.removeItem("resumeData");
  window.location.reload();
}

async function getLinkedInJobs(){
    const location = document.getElementById("locationInput").value.trim();
    if (!location) {
        alert("Please enter a location");
        return;
    }

    // keywords + location ko query params me bhej ke redirect
    const params = new URLSearchParams({
        keywords: extractedKeywords,
        location: location
    });

   window.location.href = "/job-recommendation/linkedin?" + params.toString() + "&fromHome=true";

}

async function getNaukriJobs() {
    const location = document.getElementById("locationInput").value.trim();
    if (!location) {
        alert("Please enter a location");
        return;
    }

    // keywords + location ko query params me bhej ke redirect
    const params = new URLSearchParams({
        keywords: extractedKeywords,
        location: location
    });

   window.location.href = "/job-recommendation/naukri?" + params.toString() + "&fromHome=true";

}

async function getSuggestions() {
    const resumeInput = document.getElementById("resumeFile");

    if (!resumeInput.files.length) {
        alert("Please upload a resume file");
        return;
    }

    const formData = new FormData();
    formData.append("resume_file", resumeInput.files[0]);

    const response = await fetch("/suggestions", {
        method: "POST",
        body: formData
    });

    if (response.ok) {
        const html = await response.text();
        document.open();
        document.write(html);
        document.close();
    } else {
        console.error("Error:", response.statusText);
    }
}




function resetResume() {
  localStorage.removeItem("resumeData");
  window.location.reload();
}

