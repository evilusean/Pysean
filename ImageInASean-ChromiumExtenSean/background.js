chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "downloadImages") {
    console.log("Received downloadImages message with URLs:", message.urls);
    message.urls.forEach(url => {
      const filename = url.split('/').pop();
      console.log("Downloading image:", url, "as", filename);
      chrome.downloads.download({
        url: url,
        filename: `4Chan-Unsorted/${filename}`
      }, (downloadId) => {
        if (chrome.runtime.lastError) {
          console.error("Download failed:", chrome.runtime.lastError.message);
        } else {
          console.log("Download started with ID:", downloadId);
        }
      });
    });
  }
  return true;
});