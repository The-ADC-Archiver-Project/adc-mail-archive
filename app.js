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