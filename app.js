function escapeHtml(str) {
  return str
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
}

fetch('./feed.json')
  .then(r => r.json())
  .then(data => {
    const app = document.getElementById("app")

    data.forEach(thread => {

      let itemsHtml = ""

      thread.items.forEach(item => {
        const title = escapeHtml(item.title || "")
        const content = escapeHtml(item.content || "")
        const link = item.link || "#"

        itemsHtml += `
          <div style="margin-bottom:12px;">
            <h4 style="margin:0;">
              ${title}
              <a href="${link}" target="_blank" style="margin-left:8px;">
                📧
              </a>
            </h4>

            <pre style="white-space: pre-wrap; margin-top:6px;">${content}</pre>

            <hr>
          </div>
        `
      })

      const wrapper = document.createElement("div")

      wrapper.innerHTML = `
        <details style="
          margin-bottom:12px;
          border:1px solid #ddd;
          border-radius:6px;
          padding:8px;
        ">
          <summary style="
            cursor:pointer;
            font-size:16px;
            font-weight:bold;
          ">
            ${escapeHtml(thread.thread)} (${thread.count})
          </summary>

          <div style="padding-left:12px; margin-top:10px;">
            ${itemsHtml}
          </div>
        </details>
      `

      app.appendChild(wrapper)
    })
  })
  .catch(err => {
    console.error("Failed to load feed.json:", err)
  })