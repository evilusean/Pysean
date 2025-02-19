chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "downloadImages") {
    console.log("Received downloadImages message with URLs:", message.urls);
    message.urls.forEach(url => {
      const filename = url.split('/').pop(); // Extract the filename from the URL
      console.log("Attempting download for:", url, "as", filename);
      chrome.downloads.download({
        url: url,
        filename: `/mnt/sdb4/MEmes/4Chan-Unsorted/${filename}` // Save to the specified folder
      }, (downloadId) => {
        if (chrome.runtime.lastError) {
          console.error("Download failed:", chrome.runtime.lastError.message);
        } else {
          console.log("Download started with ID:", downloadId);
        }
      });
    });
  }
});