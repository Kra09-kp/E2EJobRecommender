 // Store keywords for second API call
let extractedKeywords = [];

document.addEventListener("DOMContentLoaded", () => {
  const savedData = localStorage.getItem("resumeData");

  if (savedData) {
    const data = JSON.parse(savedData);
    extractedKeywords = data.keywords || [];

    if (extractedKeywords) {
    //   extractedKeywords = data.keywords;
      document.getElementById("result").innerHTML = `<strong>Recommended Keywords:</strong> ${extractedKeywords.join(", ")}`;
      renderButtons();
    }
      
    // if (data.keywords) {
    //   extractedKeywords = data.keywords;
    //   document.getElementById("result").innerHTML = `<strong>Recommended Keywords:</strong> ${data.keywords.join(", ")}`;
    //   renderButtons();
    // }
  }
});

async function uploadResume() {
    const fileInput = document.getElementById("resumeFile");
    const resultDiv = document.getElementById("result");

    if (fileInput.files.length === 0) {
        alert("Please select a PDF file first");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
      let extractedKeywords = [
        "Software Engineer",
        "Data Scientist",
        "Machine Learning Engineer",
        "Full Stack Developer",
        "DevOps Engineer"
    ];
    // let response = await fetch("/keywords", {
    //   method: "POST",
    //   body: formData
    // });

    // if (!response.ok) {
    //   resultDiv.innerHTML = `<span style="color: red;">Error: ${response.statusText}</span>`;
    //   return;
    // }

    // const data = await response.json();

    localStorage.setItem("resumeData", JSON.stringify({
      keywords: extractedKeywords,
      fileName: fileInput.files[0].name
    }));

    
    if (extractedKeywords) {
    //   extractedKeywords = data.keywords;
      resultDiv.innerHTML = `<strong>Recommended Keywords:</strong> ${extractedKeywords.join(", ")}`;
      renderButtons();
    } else {
      resultDiv.innerHTML = `<span style="color: yellow;">No keywords found in response.</span>`;
    }
    // if (data.keywords) {
    //   extractedKeywords = data.keywords;
    //   resultDiv.innerHTML = `<strong>Recommended Keywords:</strong> ${data.keywords.join(", ")}`;
    //   renderButtons();
    // } else {
    //   resultDiv.innerHTML = `<span style="color: yellow;">No keywords found in response.</span>`;
    // }

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

