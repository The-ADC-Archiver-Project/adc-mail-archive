function toggle(id) {
  const el = document.getElementById(id)
  if (el.style.display === "none") {
    el.style.display = "block"
  } else {
    el.style.display = "none"
  }
}

fetch('./feed.json')
  .then(r => r.json())
  .then(data => {
    const app = document.getElementById("app")

    data.forEach((thread, i) => {
      const threadId = "thread_" + i

      let html = ""

      thread.items.forEach(item => {
        html += `
          <div style="margin-bottom:10px;">
            <h4>
              ${item.title}
              <a href="${item.link}" target="_blank" style="margin-left:8px;">
                📧
              </a>
            </h4>

            <pre style="white-space: pre-wrap">${item.content}</pre>
            <hr>
          </div>
        `
      })

      const div = document.createElement("div")
      div.innerHTML = `
        <h2 style="cursor:pointer;" onclick="toggle('${threadId}')">
          ${thread.thread} (${thread.count})
        </h2>

        <div id="${threadId}" style="display:none; padding-left:15px;">
          ${html}
        </div>
      `

      app.appendChild(div)
    })
  })
  .catch(err => {
    console.error("Feed load error:", err)
  })