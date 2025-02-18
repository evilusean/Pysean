chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "downloadImages") {
      message.urls.forEach(url => {
        const filename = url.split('/').pop(); // Extract the filename from the URL
        chrome.downloads.download({
          url: url,
          filename: `/mnt/sdb4/MEmes/4Chan-Unsorted/${filename}` // Save to the specified folder
        });
      });
    }
  });