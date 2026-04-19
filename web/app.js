function escape(str) {
  return (str || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
}

function render(data) {
  const app = document.getElementById("app")
  app.innerHTML = ""

  data.forEach(thread => {

    let items = ""

    thread.items.forEach(m => {
      items += `
        <div style="margin-bottom:12px;">
          <h4>
            ${escape(m.title)}
            <a href="${m.link}" target="_blank">📧</a>
          </h4>
          <pre style="white-space:pre-wrap">${escape(m.content)}</pre>
          <hr>
        </div>
      `
    })

    const el = document.createElement("div")

    el.innerHTML = `
      <details style="margin-bottom:12px; border:1px solid #ddd; padding:8px;">
        <summary>
          ${(thread.tags || []).join(" ")} ${thread.thread} (${thread.count})
        </summary>
        <div>${items}</div>
      </details>
    `

    app.appendChild(el)
  })
}

function load() {
  fetch("../data/feed.json")
    .then(r => r.json())
    .then(d => {
      render(d)
      document.getElementById("last-update").innerText =
        "Last update: " + new Date().toLocaleTimeString()
    })
}

load()
setInterval(load, 60000)