document.getElementById('saveImages').addEventListener('click', () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.tabs.sendMessage(tabs[0].id, { action: "getImages" }, (response) => {
        console.log("Received image URLs from content script:", response.urls);
        chrome.runtime.sendMessage({ action: "downloadImages", urls: response.urls });
      });
    });
  });