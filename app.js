function escape(str) {
  return (str || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
}

function render(months) {
  const app = document.getElementById("app")
  app.innerHTML = ""

  months.slice().reverse().forEach(month => {
    const header = document.createElement("h2")
    header.textContent = month.month
    app.appendChild(header)

    // Groepeer posts in threads
    const threads = []
    const threadMap = {}

    month.posts.forEach(post => {
      // Strip [ADC], Re:, en witruimte om de thread-key te bepalen
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

    // Nieuwste thread bovenaan (op basis van laatste post in thread)
    threads.reverse().forEach(thread => {
      const el = document.createElement("div")
      el.style = "margin-bottom:12px; border:1px solid #ddd; padding:8px;"

      const items = thread.posts.map(post => `
        <div style="margin:8px 0; padding:8px; border-top:1px solid #eee;">
          <h3 style="margin:0 0 4px 0;">${escape(post.title)}</h3>
          <a href="${post.url}" target="_blank" style="margin-left:6px;">
            <!-- <img src="https://raw.githubusercontent.com/The-ADC-Archiver-Project/adc-mail-archive/refs/heads/main/assets/icon.svg" --> style="width:16px; height:16px; vertical-align:middle;" />
          </a>
          <pre style="white-space:pre-wrap; margin-top:6px;">${escape(post.body)}</pre>
        </div>
      `).join("")

      el.innerHTML = `
        <details>
          <summary>${escape(thread.key)} (${thread.posts.length})</summary>
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