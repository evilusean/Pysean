document.addEventListener('DOMContentLoaded', () => {
  const saveImagesButton = document.getElementById('saveImages');
  if (saveImagesButton) {
    saveImagesButton.addEventListener('click', () => {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, { action: "getImages" }, (response) => {
          console.log("Received image URLs from content script:", response.urls);
          chrome.runtime.sendMessage({ action: "downloadImages", urls: response.urls });
        });
      });
    });
  } else {
    console.error("Button with ID 'saveImages' not found.");
  }
});