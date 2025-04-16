document.addEventListener('DOMContentLoaded', () => {
  const saveImagesButton = document.getElementById('saveImages');
  
  if (saveImagesButton) {
    saveImagesButton.addEventListener('click', async () => {
      try {
        const tabs = await chrome.tabs.query({ currentWindow: true });
        const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
        
        if (!activeTab) {
          console.error("No active tab found");
          return;
        }

        // Valid extensions for images
        const validExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webm', '.mp4'];
        
        // Filter tabs: only those with direct image URLs from 4chan or 8kun
        const tabsToProcess = tabs.filter(tab => 
          tab.index >= activeTab.index && 
          tab.url && 
          ((tab.url.startsWith('https://i.4cdn.org/') || 
            tab.url.includes('8kun.top/') ||
            tab.url.includes('file_store/')) &&
           validExtensions.some(ext => tab.url.toLowerCase().endsWith(ext)))
        );

        console.log(`Found ${tabsToProcess.length} image tabs to process`);
        
        // Process each image tab
        for (const tab of tabsToProcess) {
          console.log(`Processing image tab: ${tab.url}`);
          try {
            const filename = tab.url.split('/').pop();
            console.log(`Downloading image: ${filename}`);
            chrome.runtime.sendMessage({
              action: "downloadImages",
              urls: [tab.url],
              tabId: tab.id  // Add the tab ID
            });
          } catch (error) {
            console.error(`Error processing tab ${tab.id}:`, error.message);
          }
        }
      } catch (error) {
        console.error("Error:", error.message);
      }
    });
  }
});