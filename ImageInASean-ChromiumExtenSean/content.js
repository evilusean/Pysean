function getImageUrls() {
    const images = document.querySelectorAll('img[src*=".jpg"], img[src*=".png"]');
    return Array.from(images)
      .map(img => img.src)
      .filter(url => url.startsWith('https://i.4cdn.org/')); // Only include image URLs
  }
  
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "getImages") {
      const urls = getImageUrls();
      sendResponse({ urls: urls });
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