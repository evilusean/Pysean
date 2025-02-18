document.addEventListener('DOMContentLoaded', () => {
  console.log("DOM fully loaded and parsed.");
  const saveImagesButton = document.getElementById('saveImages');
  if (saveImagesButton) {
    console.log("Save Images button found.");
    saveImagesButton.addEventListener('click', () => {
      console.log("Save Images button clicked.");
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        console.log("Querying active tab.");
        chrome.tabs.sendMessage(tabs[0].id, { action: "getImages" }, (response) => {
          if (chrome.runtime.lastError) {
            console.error("Error sending message to content script:", chrome.runtime.lastError);
          } else {
            console.log("Received image URLs from content script:", response.urls);
            chrome.runtime.sendMessage({ action: "downloadImages", urls: response.urls });
          }
        });
      });
    });
  } else {
    console.error("Button with ID 'saveImages' not found.");
  }
});