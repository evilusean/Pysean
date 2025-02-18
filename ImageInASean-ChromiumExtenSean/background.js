chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "downloadImages") {
      message.urls.forEach(url => {
        chrome.downloads.download({ url: url });
      });
    }
  });