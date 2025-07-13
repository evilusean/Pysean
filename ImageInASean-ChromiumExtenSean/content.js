document.addEventListener('DOMContentLoaded', () => {
  console.log("Popup DOM fully loaded.");
  const saveImagesButton = document.getElementById('saveImages');
  if (saveImagesButton) {
    console.log("Save Images button found.");
    saveImagesButton.addEventListener('click', () => {
      console.log("Save Images button clicked.");

      // First, get all tabs in the current window
      chrome.tabs.query({ currentWindow: true }, (tabs) => {
        // Then, get the active tab so we know where to start
        chrome.tabs.query({ active: true, currentWindow: true }, (activeTabs) => {
          if (activeTabs.length === 0) {
            console.error("No active tab found.");
            return;
          }
          const activeIndex = activeTabs[0].index;
          console.log("Active tab index:", activeIndex);

          // Filter tabs whose index is equal to or greater than the active tab index,
          // and also ensure they are 4chan or 8kun boards pages.
          const tabsToProcess = tabs.filter(tab => {
            return tab.index >= activeIndex && 
                  tab.url && 
                  (tab.url.includes("boards.4chan.org") || 
                   tab.url.includes("8kun.top"));
          });
          console.log("Tabs to process:", tabsToProcess);

          // Iterate over the selected tabs and send message to get images
          tabsToProcess.forEach(tab => {
            chrome.tabs.sendMessage(tab.id, { action: "getImages" }, (response) => {
              if (chrome.runtime.lastError) {
                console.error(`Error sending message to tab ${tab.id}:`, chrome.runtime.lastError);
              } else if (response) {
                console.log(`Received images from tab ${tab.id}:`, response.urls);
                // Send each tab's images to background for download
                chrome.runtime.sendMessage({ action: "downloadImages", urls: response.urls });
              } else {
                console.warn(`No response from tab ${tab.id}.`);
              }
            });
          });
        });
      });
    });
  } else {
    console.error("Button with ID 'saveImages' not found.");
  }
});

console.log("Content script loaded");

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log("Message received in content script:", request);
  
  if (request.action === "getImages") {
    try {
      const images = document.querySelectorAll('img[src*=".jpg"], img[src*=".png"], img[src*=".jpeg"], img[src*=".gif"]');
      const urls = Array.from(images)
        .map(img => img.src)
        .filter(url => 
          url.startsWith('https://i.4cdn.org/') || 
          url.includes('8kun.top/') ||
          url.includes('file_store/')
        );
      
      console.log(`Found ${urls.length} images`);
      sendResponse({ urls: urls });
    } catch (error) {
      console.error('Error in content script:', error);
      sendResponse({ error: error.message });
    }
    return true;  // Keep the message port open
  }

  // New: Scrape all media from thread
  if (request.action === "getThreadMedia") {
    try {
      // Images (not thumbnails for videos)
      const imgUrls = Array.from(document.querySelectorAll('img[src]'))
        .map(img => img.src)
        .filter(url => url.match(/\.(jpg|jpeg|png|gif)$/i) && url.startsWith('https://i.4cdn.org/'));
      // Webms/mp4s (from <a> and <source> tags)
      const videoUrls = Array.from(document.querySelectorAll('a[href], source[src]'))
        .map(el => el.href || el.src)
        .filter(url => url && url.match(/\.(webm|mp4)$/i) && url.startsWith('https://i.4cdn.org/'));
      // Remove video thumbnails from imgUrls
      const videoThumbs = videoUrls.map(url => url.replace(/\.(webm|mp4)$/i, 's.jpg'));
      const filteredImgUrls = imgUrls.filter(url => !videoThumbs.includes(url));
      // Combine and dedupe
      const allUrls = Array.from(new Set([...filteredImgUrls, ...videoUrls]));
      console.log(`Found ${allUrls.length} media files in thread`);
      sendResponse({ urls: allUrls });
    } catch (error) {
      console.error('Error scraping thread media:', error);
      sendResponse({ error: error.message });
    }
    return true;
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