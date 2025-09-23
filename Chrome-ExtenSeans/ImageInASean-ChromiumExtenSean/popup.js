document.addEventListener('DOMContentLoaded', () => {
  console.log("Popup DOM loaded");
  const saveImagesButton = document.getElementById('saveImages');
  const saveThreadMediaButton = document.getElementById('saveThreadMedia');
  
  const saveThreadHtmlButton = document.getElementById('saveThreadHtml');


  if (saveThreadHtmlButton) {
    saveThreadHtmlButton.addEventListener('click', async () => {
      try {
        const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
        if (!activeTab) {
          alert("No active tab found");
          return;
        }
        const threadUrl = activeTab.url;
        const threadMatch = threadUrl.match(/boards\.4chan\.org\/(\w+)\/thread\/(\d+)/);
        if (!threadMatch) {
          alert("Not a 4chan thread page!");
          return;
        }
        const board = threadMatch[1];
        const threadId = threadMatch[2];
        // Ask content script for all posts and media
        const response = await chrome.tabs.sendMessage(activeTab.id, { action: "getThreadFull" });
        if (!response || !response.posts || response.posts.length === 0) {
          alert("No posts found in thread!");
          return;
        }
        // Build HTML
        let html = `<!DOCTYPE html><html><head><meta charset='utf-8'><title>/${board}/ - ${threadId}</title><style>body{font-family:sans-serif;background:#f8f8f8;} .post{border:1px solid #ccc;background:#fff;margin:10px;padding:10px;border-radius:6px;} .media{margin:5px 0;} .postnum{color:#888;font-size:0.9em;} .reply{color:#06c;text-decoration:underline;cursor:pointer;} img,video{max-width:400px;display:block;margin:5px 0;}</style></head><body>`;
        html += `<h2>/${board}/ - Thread ${threadId}</h2>`;
        response.posts.forEach(post => {
          html += `<div class='post'><div class='postnum'>No.${post.no} | ${post.name || ''} ${post.time || ''}</div>`;
          html += `<div>${post.com || ''}</div>`;
          let statusDiv = document.getElementById('status');
          if (!statusDiv) {
            statusDiv = document.createElement('div');
            statusDiv.id = 'status';
            document.body.appendChild(statusDiv);
          }

          function setStatus(msg, isError) {
            statusDiv.textContent = msg;
            statusDiv.style.color = isError ? 'red' : 'green';
          }
          if (post.media && post.media.length) {
            post.media.forEach(url => {
              if (url.match(/\.(jpg|jpeg|png|gif)$/i)) {
                html += `<div class='media'><a href='${url}' target='_blank'><img src='${url}'></a></div>`;
              } else if (url.match(/\.(webm|mp4)$/i)) {
                html += `<div class='media'><a href='${url}' target='_blank'><video src='${url}' controls></video></a></div>`;
              }
            });
          }
          html += `</div>`;
        });
        html += `</body></html>`;
        // Save HTML file
        const blob = new Blob([html], {type: 'text/html'});
        const filename = `4chan-thread-${board}-${threadId}.html`;
        const url = URL.createObjectURL(blob);
        chrome.downloads.download({
          url,
          filename,
          saveAs: true
        });
        alert(`Saved thread as HTML: ${filename}`);
      } catch (error) {
        console.error("Error saving thread as HTML:", error);
        alert("Failed to save thread as HTML. See console for details.");
      }
    });
}

  if (saveImagesButton) {
    saveImagesButton.addEventListener('click', async () => {
      try {
        const tabs = await chrome.tabs.query({ currentWindow: true });
        const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
        if (!activeTab) {
          console.error("No active tab found");
          return;
        }
        const validExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webm', '.mp4'];
        const tabsToProcess = tabs.filter(tab => {
          if (!tab.url || tab.index < activeTab.index) return false;
          const is4ChanImage = tab.url.startsWith('https://i.4cdn.org/') && 
                               validExtensions.some(ext => tab.url.toLowerCase().endsWith(ext));
          const is8KunImage = tab.url.includes('8kun.top') && 
                              tab.url.includes('file_store') && 
                              validExtensions.some(ext => tab.url.toLowerCase().endsWith(ext));
          return is4ChanImage || is8KunImage;
        });
        if (tabsToProcess.length === 0) {
          console.log("No image tabs found to process");
          return;
        }
        const allUrls = tabsToProcess.map(tab => tab.url);
        const tabIds = tabsToProcess.map(tab => tab.id);
        await chrome.runtime.sendMessage({
          action: "downloadImages",
          urls: allUrls,
          tabIds: tabIds
        });
      } catch (error) {
        console.error("Error in main process:", error.message);
      }
    });
  } else {
    console.error("Save Images button not found");
  }