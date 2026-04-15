fetch('./feed.json')
  .then(r => r.json())
  .then(data => {
    const app = document.getElementById("app")

    data.forEach(thread => {
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
        <h2>${thread.thread}</h2>
        ${html}
      `

      app.appendChild(div)
    })
  })