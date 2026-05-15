function escape(str) {
  return (str || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
}

function extractQuotedText(body) {
  const lines = body.split("\n");
  let mainContent = [];
  let quotedContent = [];
  let inQuote = false;
  
  for (let line of lines) {
    if (line.trim().startsWith(">") || line.trim().startsWith("|")) {
      inQuote = true;
      quotedContent.push(line);
    } else if (inQuote && line.trim() === "") {
      quotedContent.push(line);
    } else if (line.match(/^Op \d+-\d+-\d+/) || line.match(/^On \d+-\d+-\d+/) || line.trim() === "") {
      if (!inQuote) mainContent.push(line);
      else quotedContent.push(line);
    } else {
      if (inQuote && mainContent.length === 0) {
        inQuote = false;
      }
      mainContent.push(line);
    }
  }
  
  return {
    main: mainContent.join("\n").trim(),
    quoted: quotedContent.join("\n").trim()
  };
}

function formatTimestamp(timestamp) {
  if (!timestamp || !Array.isArray(timestamp) || timestamp.length < 6) {
    return "Unknown date";
  }
  const [year, month, day, hour, minute, second] = timestamp;
  const date = new Date(year, month - 1, day, hour, minute, second);
  return date.toLocaleDateString('nl-NL', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function render(months) {
  const app = document.getElementById("app")
  app.innerHTML = ""

  months.slice().reverse().forEach(month => {
    const header = document.createElement("h2")
    header.style = "margin-top: 20px; padding-bottom: 8px; border-bottom: 2px solid #0066cc;"
    header.textContent = month.month
    app.appendChild(header)

    const threads = []
    const threadMap = {}

    month.posts.forEach(post => {
      const key = post.title
        .replace(/\[ADC\]/gi, "")
        .replace(/^(\s*Re:\s*)*/i, "")
        .trim()

      if (!threadMap[key]) {
        threadMap[key] = { key, posts: [] }
        threads.push(threadMap[key])
      }
      threadMap[key].posts.push(post)
    })

    threads.reverse().forEach(thread => {
      const el = document.createElement("div")
      el.style = "margin-bottom: 16px; border: 1px solid #ddd; border-radius: 4px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1);"

      const items = thread.posts.map((post, idx) => {
        const { main, quoted } = extractQuotedText(post.body);
        const isReply = post.title.toLowerCase().includes("re:");
        const indent = isReply ? "20px" : "0px";
        const bgColor = isReply ? "#f9f9f9" : "#fff";
        
        return `
          <div style="margin: 0; padding: 12px 16px; border-top: ${idx > 0 ? '2px solid #e0e0e0' : 'none'}; background-color: ${bgColor}; margin-left: ${indent};">
            <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px;">
              <h3 style="margin: 0; font-size: 1em; color: #333;">
                ${isReply ? '↳ ' : ''}${escape(post.title)}
              </h3>
              <span style="font-size: 0.85em; color: #666; flex-shrink: 0; margin-left: 12px;">
                ${formatTimestamp(post.timestamp)}
              </span>
            </div>
            <div style="color: #666; font-size: 0.9em; margin-bottom: 10px;">
              ${main ? `<pre style="white-space: pre-wrap; word-wrap: break-word; margin: 8px 0; padding: 8px; background: #f5f5f5; border-left: 3px solid #0066cc; border-radius: 2px;">${escape(main)}</pre>` : ''}
              ${quoted ? `<details style="margin-top: 8px; padding: 8px; background: #f0f0f0; border-radius: 2px; cursor: pointer;">
                <summary style="color: #666; font-size: 0.9em;">Show quoted text (${quoted.split('\n').length} lines)</summary>
                <pre style="white-space: pre-wrap; word-wrap: break-word; margin: 8px 0 0 0; font-size: 0.9em; color: #888;">${escape(quoted)}</pre>
              </details>` : ''}
            </div>
          </div>
        `
      }).join("")

      el.innerHTML = `
        <details open>
          <summary style="padding: 12px 16px; background: #f5f5f5; cursor: pointer; font-weight: bold; user-select: none;">
            ${escape(thread.key)} 
            <span style="color: #666; font-weight: normal; margin-left: 8px;">(${thread.posts.length} message${thread.posts.length !== 1 ? 's' : ''})</span>
          </summary>
          ${items}
        </details>
      `
      app.appendChild(el)
    })
  })
}

function load() {
  fetch("./data/feed.json")
    .then(r => r.json())
    .then(d => {
      render(d.months)
      document.getElementById("last-update").innerText =
        "Last update: " + new Date().toLocaleTimeString()
    })
    .catch(err => console.error("load error:", err))
}

load()
setInterval(load, 60000)