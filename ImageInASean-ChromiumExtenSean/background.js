chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "downloadImages") {
      message.urls.forEach(url => {
        const filename = url.split('/').pop(); // Extract the filename from the URL
        chrome.downloads.download({
          url: url,
          filename: `4chan_images/${filename}` // Save to a folder named '4chan_images'
        });
      });
    }
  });