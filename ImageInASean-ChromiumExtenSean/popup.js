document.addEventListener('DOMContentLoaded', () => {
  console.log("Popup DOM fully loaded and parsed.");
  const saveImagesButton = document.getElementById('saveImages');
  if (saveImagesButton) {
    console.log("Save Images button found.");
    saveImagesButton.addEventListener('click', () => {
      console.log("Save Images button clicked.");
      // Get all tabs in the current window
      chrome.tabs.query({ currentWindow: true }, (tabs) => {
        // Get the active tab
        chrome.tabs.query({ active: true, currentWindow: true }, ([activeTab]) => {
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
          
          tabsToProcess.forEach(tab => {
            console.log(`Processing tab: ${tab.url}`);
            chrome.tabs.sendMessage(tab.id, { action: "getImages" }, response => {
              if (chrome.runtime.lastError) {
                console.error(`Error with tab ${tab.id}:`, chrome.runtime.lastError);
                return;
              }
              if (response && response.urls && response.urls.length > 0) {
                console.log(`Found ${response.urls.length} images in tab ${tab.id}`);
                chrome.runtime.sendMessage({
                  action: "downloadImages",
                  urls: response.urls
                });
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