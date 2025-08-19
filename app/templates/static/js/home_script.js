let extractedKeywords = [
    "Software Engineer",
    "Data Scientist",
    "Machine Learning Engineer",
    "Full Stack Developer",
    "DevOps Engineer"
]; // Store keywords for second API call

async function uploadResume() {
    const fileInput = document.getElementById("resumeFile");
    const resultDiv = document.getElementById("result");
    const nextStepDiv = document.getElementById("nextStep");

    if (fileInput.files.length === 0) {
        alert("Please select a PDF file first");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        resultDiv.innerHTML = `<span style="color: yellow;">Everthing is fine here.</span>`;

        nextStepDiv.innerHTML = `
            <input type="text" id="locationInput" placeholder="Enter location" style="padding:6px; border-radius:4px; margin-right:8px;">
            <button type="button" onclick="getLinkedInJobs()">Get Job Recommendations</button>
        `

        // Simulate a delay to mimic file processing
        // await new Promise(resolve => setTimeout(resolve, 1000));

        // Call the second API
        // let response = await fetch("/job-recommendation", {
        //     method: "POST",
        //     body: formData
        // });
        
        // if (!response.ok) {
        //     resultDiv.innerHTML = `<span style="color: red;">Error: ${response.statusText}</span>`;
        //     return;
        // }

        // const data = await response.json();

        // if (data.keywords) {
        //     extractedKeywords = data.keywords;
        //     resultDiv.innerHTML = `<strong>Recommended Keywords:</strong> ${data.keywords.join(", ")}`;

        //     // Show button to get LinkedIn jobs
        //     nextStepDiv.innerHTML = `
        //     <input type="text" id="locationInput" placeholder="Enter location" style="padding:6px; border-radius:4px; margin-right:8px;">
        //     <button type="button" onclick="getLinkedInJobs()">Get Job Recommendations</button>
        // `;
        // } else {
        //     resultDiv.innerHTML = `<span style="color: yellow;">No keywords found in response.</span>`;
        // }
    } catch (error) {
        resultDiv.innerHTML = `<span style="color: red;">Error: ${error.message}</span>`;
    }
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

    window.location.href = "/job-recommendation/naukri?" + params.toString();
}


//     try {

//         let response = await fetch("/job-recommendation/linkedin", {
//             method: "POST",
//             headers: {
//         "Content-Type": "application/json"
//             },
//             body: JSON.stringify({ keywords: extractedKeywords, location: location })
//         });


//         if (!response.ok) {
//             resultDiv.innerHTML += `<br><span style="color: red;">Error: ${response.statusText}</span>`;
//             return;
//         }

//         const jobs = await response.json();

//         if (Array.isArray(jobs) && jobs.length > 0) {
//             resultDiv.innerHTML += `<br><br><strong>Job Recommendations:</strong><ul>` +
//                 jobs.map(job => `<li>${job}</li>`).join("") +
//                 `</ul>`;
//         } else {
//             resultDiv.innerHTML += `<br><span style="color: yellow;">No job recommendations found.</span>`;
//         }
//     } catch (error) {
//         resultDiv.innerHTML += `<br><span style="color: red;">Error: ${error.message}</span>`;
//     }





