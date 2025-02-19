document.addEventListener('DOMContentLoaded', () => {
  const saveImagesButton = document.getElementById('saveImages');
  
  if (saveImagesButton) {
    saveImagesButton.addEventListener('click', async () => {
      try {
        // Get all tabs and find active tab
        const tabs = await chrome.tabs.query({ currentWindow: true });
        const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
        
        if (!activeTab) {
          console.error("No active tab found");
          return;
        }

        // Filter tabs to process
        const tabsToProcess = tabs.filter(tab => 
          tab.index >= activeTab.index && 
          tab.url && 
          tab.url.includes("boards.4chan.org")
        );

        console.log(`Found ${tabsToProcess.length} tabs to process`);
        
        // Process each tab
        for (const tab of tabsToProcess) {
          console.log(`Processing tab ${tab.id}: ${tab.url}`);
          
          // Inject content script if needed
          try {
            await chrome.scripting.executeScript({
              target: { tabId: tab.id },
              files: ['content.js']
            });
          } catch (err) {
            console.log(`Content script already injected in tab ${tab.id}`);
          }

          // Get images from tab
          try {
            const response = await new Promise((resolve, reject) => {
              chrome.tabs.sendMessage(tab.id, { action: "getImages" }, response => {
                if (chrome.runtime.lastError) {
                  console.error(`Tab ${tab.id} error:`, chrome.runtime.lastError);
                  reject(chrome.runtime.lastError);
                } else {
                  resolve(response);
                }
              });
            });

            if (response?.urls?.length > 0) {
              console.log(`Found ${response.urls.length} images in tab ${tab.id}`);
              chrome.runtime.sendMessage({
                action: "downloadImages",
                urls: response.urls
              });
            } else {
              console.log(`No images found in tab ${tab.id}`);
            }
          } catch (error) {
            console.error(`Error processing tab ${tab.id}:`, error);
          }
        }
      } catch (error) {
        console.error("Error:", error);
      }
    });
  }
});