// SCRAPE
document.getElementById("scrape-btn").addEventListener("click", () => {
    const url = document.getElementById("scrape-url").value;
    document.getElementById("scrape-status").innerText = "Scraping...";
    fetch("/scrape", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("scrape-status").innerText = data.message;
        const list = document.getElementById("scraped-urls");
        list.innerHTML = "";
        data.scraped_urls.forEach(link => {
            const li = document.createElement("li");
            li.textContent = link;
            list.appendChild(li);
        });
    });
});

// FETCH
document.getElementById("fetch-btn").addEventListener("click", () => {
    const url = document.getElementById("fetch-url").value;
    fetch("/fetch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        document.getElementById("article-display").style.display = "block";
        document.getElementById("article-title").innerText = data.title;
        document.getElementById("article-date").innerText = data.date;
        document.getElementById("article-text").innerHTML = `<strong>${data.title}</strong><br><br><strong>Date:</strong> ${data.date}<br><br>${data.text}`;
        document.getElementById("article-summary").value = "";
        document.getElementById("article-image").src = data.image_path ? `/images/${data.image_path.split('/').pop()}` : "";
    });
});

// SUMMARIZE
document.getElementById("summarize-btn").addEventListener("click", () => {
    // Extract only the article text without title/date formatting
    const rawText = document.getElementById("article-text").innerText;

    if (!rawText) return;

    document.getElementById("article-summary").value = "Summarizing...";

    fetch("/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: rawText })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("article-summary").value = data.summary;
    });
});
