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
        let response;
        try {
          response = await new Promise((resolve, reject) => {
            chrome.tabs.sendMessage(activeTab.id, { action: "getThreadFull" }, (resp) => {
              if (chrome.runtime.lastError) {
                reject(chrome.runtime.lastError.message);
              } else {
                resolve(resp);
              }
            });
          });
        } catch (err) {
          alert("Could not connect to content script. Try reloading the thread page after reloading the extension.\nError: " + err);
          return;
        }
        if (!response || !response.posts || response.posts.length === 0) {
          alert("No posts found in thread! If this is a 4chan thread, try reloading the page after reloading the extension.");
          return;
        }
        // Gather all unique media URLs
        let allMedia = [];
        response.posts.forEach(post => {
          if (post.media && post.media.length) {
            post.media.forEach(url => {
              if (!allMedia.includes(url)) allMedia.push(url);
            });
          }
        });
        // Download all media to thread folder, then save HTML after a short delay
        let htmlFolder = '';
        if (allMedia.length > 0) {
          await chrome.runtime.sendMessage({
            action: "downloadThreadMedia",
            urls: allMedia,
            threadId: threadId
          });
          htmlFolder = `4Chan-${threadId}/`;
          // Wait a moment to help ensure folder is created
          await new Promise(res => setTimeout(res, 800));
        }
        // Build HTML referencing local files
        let html = `<!DOCTYPE html><html><head><meta charset='utf-8'><title>/${board}/ - ${threadId}</title><style>body{font-family:sans-serif;background:#f8f8f8;} .post{border:1px solid #ccc;background:#fff;margin:10px;padding:10px;border-radius:6px;} .media{margin:5px 0;} .postnum{color:#888;font-size:0.9em;} .reply{color:#06c;text-decoration:underline;cursor:pointer;} img,video{max-width:400px;display:block;margin:5px 0;}</style></head><body>`;
        html += `<h2>/${board}/ - Thread ${threadId}</h2>`;
        response.posts.forEach(post => {
          html += `<div class='post'><div class='postnum'>No.${post.no} | ${post.name || ''} ${post.time || ''}</div>`;
          html += `<div>${post.com || ''}</div>`;
          if (post.media && post.media.length) {
            post.media.forEach(url => {
              const filename = url.split('/').pop();
              const localPath = `${htmlFolder}${filename}`;
              if (url.match(/\.(jpg|jpeg|png|gif)$/i)) {
                html += `<div class='media'><a href='${localPath}' target='_blank'><img src='${localPath}'></a></div>`;
              } else if (url.match(/\.(webm|mp4)$/i)) {
                html += `<div class='media'><a href='${localPath}' target='_blank'><video src='${localPath}' controls></video></a></div>`;
              }
            });
          }
          html += `</div>`;
        });
        html += `</body></html>`;
        // Save HTML file
        // Send HTML content to background for download
        chrome.runtime.sendMessage({
          action: "downloadThreadHtml",
          htmlContent: html,
          threadId: threadId
        }, (resp) => {
          if (resp && resp.success) {
            alert(`Saved thread as HTML: thread-${threadId}.html\nAll media saved to 4Chan-${threadId}/\n\nTo archive, move this HTML file and the entire 4Chan-${threadId} folder together to any location. The links will always work as long as you keep them together.`);
          } else {
            alert("Failed to save thread as HTML. See console for details.");
          }
        });
      } catch (error) {
        console.error("Error saving thread as HTML:", error);
        alert("Failed to save thread as HTML. See console for details.");
      }
    });
  }

  if (saveThreadMediaButton) {
    saveThreadMediaButton.addEventListener('click', async () => {
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
        // Ask content script to scrape all media URLs
        let response;
        try {
          response = await new Promise((resolve, reject) => {
            chrome.tabs.sendMessage(activeTab.id, { action: "getThreadMedia" }, (resp) => {
              if (chrome.runtime.lastError) {
                reject(chrome.runtime.lastError.message);
              } else {
                resolve(resp);
              }
            });
          });
        } catch (err) {
          alert("Could not connect to content script. Try reloading the thread page after reloading the extension.\nError: " + err);
          return;
        }
        if (!response || !response.urls || response.urls.length === 0) {
          alert("No media found in thread! If this is a 4chan thread, try reloading the page after reloading the extension.");
          return;
        }
        // Send to background for batch download to thread folder
        await chrome.runtime.sendMessage({
          action: "downloadThreadMedia",
          urls: response.urls,
          threadId: threadId
        });
        alert(`Started downloading ${response.urls.length} files to folder 4Chan-${threadId}`);
      } catch (error) {
        console.error("Error in Save Thread Media:", error);
        alert("Failed to save thread media. See console for details.");
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
  }});