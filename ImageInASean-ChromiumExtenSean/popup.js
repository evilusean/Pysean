document.addEventListener('DOMContentLoaded', () => {
  console.log("Popup DOM loaded");
  const saveImagesButton = document.getElementById('saveImages');
  const saveThreadMediaButton = document.getElementById('saveThreadMedia');
  
  if (saveImagesButton) {
    console.log("Save Images button found, adding click listener");
    saveImagesButton.addEventListener('click', async () => {
      console.log("Save Images button clicked - starting process");
      
      try {
        const tabs = await chrome.tabs.query({ currentWindow: true });
        console.log(`Found ${tabs.length} total tabs`);
        
        const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
        
        if (!activeTab) {
          console.error("No active tab found");
          return;
        }
        
        console.log("Active tab:", activeTab.url);

        // Valid extensions for images
        const validExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webm', '.mp4'];
        
        // Filter tabs: only those with direct image URLs from 4chan or 8kun
        const tabsToProcess = tabs.filter(tab => {
          if (!tab.url || tab.index < activeTab.index) return false;
          
          // Check for 4chan image URLs
          const is4ChanImage = tab.url.startsWith('https://i.4cdn.org/') && 
                               validExtensions.some(ext => tab.url.toLowerCase().endsWith(ext));
          
          // Check for 8kun image URLs
          const is8KunImage = tab.url.includes('8kun.top') && 
                              tab.url.includes('file_store') && 
                              validExtensions.some(ext => tab.url.toLowerCase().endsWith(ext));
          
          // Log for debugging
          console.log(`Tab URL: ${tab.url}, is4Chan: ${is4ChanImage}, is8kun: ${is8KunImage}`);
          
          return is4ChanImage || is8KunImage;
        });

        console.log(`Found ${tabsToProcess.length} image tabs to process:`, tabsToProcess.map(t => t.url));
        
        if (tabsToProcess.length === 0) {
          console.log("No image tabs found to process");
          return;
        }
        
        // Collect all URLs for batch processing
        const allUrls = tabsToProcess.map(tab => tab.url);
        const tabIds = tabsToProcess.map(tab => tab.id);
        
        console.log(`Preparing to download ${allUrls.length} images in batch`);
        
        // Send all URLs to background script for batch download
        console.log("Sending batch download request to background script...");
        await chrome.runtime.sendMessage({
          action: "downloadImages",
          urls: allUrls,
          tabIds: tabIds
        });
        
        console.log("Batch download request sent successfully");
      } catch (error) {
        console.error("Error in main process:", error.message);
      }
    });
  } else {
    console.error("Save Images button not found");
  }

  // New: Save Thread Media button logic
  if (saveThreadMediaButton) {
    saveThreadMediaButton.addEventListener('click', async () => {
      console.log("Save Thread Media button clicked");
      try {
        const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
        if (!activeTab) {
          console.error("No active tab found");
          return;
        }
        const threadUrl = activeTab.url;
        // Check if it's a 4chan thread URL
        const threadMatch = threadUrl.match(/boards\.4chan\.org\/(\w+)\/thread\/(\d+)/);
        if (!threadMatch) {
          alert("Not a 4chan thread page!");
          return;
        }
        const board = threadMatch[1];
        const threadId = threadMatch[2];
        console.log(`Detected thread: /${board}/, ID: ${threadId}`);
        // Ask content script to scrape all media URLs
        const response = await chrome.tabs.sendMessage(activeTab.id, { action: "getThreadMedia" });
        if (!response || !response.urls || response.urls.length === 0) {
          alert("No media found in thread!");
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
});