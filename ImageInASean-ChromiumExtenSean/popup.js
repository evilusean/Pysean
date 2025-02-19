document.addEventListener('DOMContentLoaded', () => {
  console.log("Popup DOM fully loaded and parsed.");
  const saveImagesButton = document.getElementById('saveImages');
  if (saveImagesButton) {
    console.log("Save Images button found.");
    saveImagesButton.addEventListener('click', () => {
      console.log("Save Images button clicked.");
      // Get all tabs in current window
      chrome.tabs.query({ currentWindow: true }, (tabs) => {
        // Find the active tab first
        chrome.tabs.query({ active: true, currentWindow: true }, (activeTabs) => {
          if (activeTabs.length === 0) {
            console.error("No active tab found.");
            return;
          }
          const activeIndex = activeTabs[0].index;
          console.log("Active tab index:", activeIndex);
          
          // Filter tabs to process: only those that are on boards.4chan.org and to the right of (or equal to) the active tab
          const tabsToProcess = tabs.filter(tab => {
            return tab.index >= activeIndex && tab.url && tab.url.includes("boards.4chan.org");
          });
          console.log("Tabs to process:", tabsToProcess);
  
          // Iterate over each valid tab and send a message to the content script
          tabsToProcess.forEach(tab => {
            console.log(`Sending getImages message to tab id ${tab.id} with URL: ${tab.url}`);
            chrome.tabs.sendMessage(tab.id, { action: "getImages" }, (response) => {
              if (chrome.runtime.lastError) {
                console.error(`Error sending message to tab ${tab.id}:`, chrome.runtime.lastError.message);
              } else if (response) {
                console.log(`Received image URLs from tab ${tab.id}:`, response.urls);
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