function getImageUrls() {
    const images = document.querySelectorAll('img[src*=".jpg"], img[src*=".png"]');
    return Array.from(images).map(img => img.src);
  }
  
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "getImages") {
      const urls = getImageUrls();
      sendResponse({ urls: urls });
    }
  });