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
    month.posts.slice().reverse().forEach(post => {
      const el = document.createElement("div")
      el.style = "margin-bottom:12px; border:1px solid #ddd; padding:8px;"
      el.innerHTML = `
        <details>
          <summary>${escape(post.title)}</summary>
          <p><a href="${post.url}" target="_blank">📧 Open origineel</a></p>
          <pre style="white-space:pre-wrap">${escape(post.body)}</pre>
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