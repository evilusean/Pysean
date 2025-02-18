chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "downloadImages") {
      console.log("Received downloadImages message with URLs:", message.urls);
      message.urls.forEach(url => {
        const filename = url.split('/').pop(); // Extract the filename from the URL
        console.log("Downloading image:", url, "to filename:", filename);
        chrome.downloads.download({
          url: url,
          filename: `/mnt/sdb4/MEmes/4Chan-Unsorted/${filename}` // Save to the specified folder
        }, (downloadId) => {
          if (chrome.runtime.lastError) {
            console.error("Download failed:", chrome.runtime.lastError);
          } else {
            console.log("Download started with ID:", downloadId);
          }
        });
      });
    }
  });
/*
TODO : Inspect 4chan post elements, so we aren't saving every image of currently
  ongoing posts, and we are ONLY saving images I've opened in seperate tabs
This script will now only include image URLs that start with https://i.4cdn.org/, 
// effectively filtering out any URLs that contain /thread/.

To save the images to a folder, you can modify the background.js script to specify a 
filename and directory for each download. Here's an updated version of background.js
  */