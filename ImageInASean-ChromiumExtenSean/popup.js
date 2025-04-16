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
        const tabsToProcess = tabs.filter(tab => {
          // Check if URL exists
          if (!tab.url) return false;
          
          // Check if tab index is valid
          if (tab.index < activeTab.index) return false;
          
          // Check for 4chan URLs
          const is4ChanImage = tab.url.startsWith('https://i.4cdn.org/');
          
          // Check for 8kun URLs - be more specific with domain checks
          const is8KunImage = (
            tab.url.includes('8kun.top/') || 
            tab.url.includes('nerv.8kun.top/') || 
            tab.url.includes('file_store/')
          );
          
          // Check for valid extensions
          const hasValidExtension = validExtensions.some(ext => 
            tab.url.toLowerCase().endsWith(ext)
          );
          
          // Log each tab evaluation for debugging
          console.log(`Tab URL: ${tab.url}, is4ChanImage: ${is4ChanImage}, is8KunImage: ${is8KunImage}, hasValidExtension: ${hasValidExtension}`);
          
          return (is4ChanImage || is8KunImage) && hasValidExtension;
        });

        console.log(`Found ${tabsToProcess.length} image tabs to process:`, tabsToProcess.map(t => t.url));
        
        // Process each image tab
        for (const tab of tabsToProcess) {
          console.log(`Processing image tab ${tab.id}: ${tab.url}`);
          try {
            const filename = tab.url.split('/').pop();
            console.log(`Downloading image: ${filename}`);
            chrome.runtime.sendMessage({
              action: "downloadImages",
              urls: [tab.url],
              tabId: tab.id  // Pass the tab ID for closing
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