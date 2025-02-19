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

        const tabsToProcess = tabs.filter(tab => 
          tab.index >= activeTab.index && 
          tab.url && 
          tab.url.includes("boards.4chan.org")
        );

        console.log(`Processing ${tabsToProcess.length} tabs`);
        
        for (const tab of tabsToProcess) {
          console.log(`Processing tab: ${tab.url}`);
          try {
            const response = await new Promise((resolve, reject) => {
              chrome.tabs.sendMessage(tab.id, { action: "getImages" }, response => {
                if (chrome.runtime.lastError) {
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