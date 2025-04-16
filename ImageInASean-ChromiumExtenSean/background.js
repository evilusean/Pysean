const downloadedFiles = new Set();
const DOWNLOAD_PATH = '4Chan-Unsorted';
const VALID_EXTENSIONS = ['.jpg', '.png', '.gif', '.webm', '.mp4', '.jpeg'];
// webm/mp4 doesn't work, future sean problem, I'm happy with this, for now

// Valid image hosts and patterns
const VALID_HOSTS = ['i.4cdn.org'];
const VALID_PATTERNS = [
  /^https?:\/\/i\.4cdn\.org\/.+\.(jpg|jpeg|png|gif|webm|mp4)$/i,
  /^https?:\/\/nerv\.8kun\.top\/file_store\/.+\.(jpg|jpeg|png|gif|webm|mp4)$/i,
  /^https?:\/\/media\.8kun\.top\/.+\.(jpg|jpeg|png|gif|webm|mp4)$/i,
  /^https?:\/\/.+\.8kun\.top\/file_store\/.+\.(jpg|jpeg|png|gif|webm|mp4)$/i
];

function closeImageTabs() {
  console.log("Attempting to close image tabs...");
  chrome.tabs.query({ currentWindow: true }, (tabs) => {
    const imageTabIds = tabs
      .filter(tab => {
        const isValid = tab.url && isValidImageUrl(tab.url);
        console.log(`Tab URL: ${tab.url}, isValid: ${isValid}`);
        return isValid;
      })
      .map(tab => tab.id);
    
    console.log(`Found ${imageTabIds.length} image tabs to close:`, imageTabIds);
    
    if (imageTabIds.length > 0) {
      imageTabIds.forEach(tabId => {
        chrome.tabs.remove(tabId, () => {
          if (chrome.runtime.lastError) {
            console.log(`Tab ${tabId} already closed or doesn't exist: ${chrome.runtime.lastError.message}`);
          } else {
            console.log(`Closed tab ${tabId}`);
          }
        });
      });
    }
  });
}

function isValidImageUrl(url) {
  if (!url) return false;
  
  // Use regex patterns for more precise matching
  const matchesPattern = VALID_PATTERNS.some(pattern => pattern.test(url));
  console.log(`URL: ${url}, matchesPattern: ${matchesPattern}`);
  
  if (matchesPattern) {
    return true;
  }
  
  // Fallback to the old method if pattern matching fails
  const hasValidHost = VALID_HOSTS.some(host => url.includes(host));
  const hasValidExtension = VALID_EXTENSIONS.some(ext => url.toLowerCase().endsWith(ext));
  
  console.log(`URL: ${url}, hasValidHost: ${hasValidHost}, hasValidExtension: ${hasValidExtension}`);
  
  return hasValidHost && hasValidExtension;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "downloadImages") {
    console.log("Received downloadImages message with URLs:", message.urls);
    let downloadCount = 0;
    const totalDownloads = message.urls.length;
    
    // If a specific tab ID is provided, store it for closing later
    const tabIdsToClose = message.tabId ? [message.tabId] : [];
    
    message.urls.forEach(url => {
      const filename = url.split('/').pop();
      
      if (downloadedFiles.has(filename)) {
        console.log(`Skipping duplicate image: ${filename}`);
        downloadCount++;
        if (downloadCount === totalDownloads) {
          setTimeout(() => {
            if (tabIdsToClose.length > 0) {
              closeSpecificTabs(tabIdsToClose);
            } else {
              closeImageTabs();
            }
          }, 1000);
        }
        return;
      }
      
      console.log("Downloading image:", url, "as", filename);
      chrome.downloads.download({
        url: url,
        filename: `${DOWNLOAD_PATH}/${filename}`,  // Save to 4Chan-Unsorted subfolder
        conflictAction: 'uniquify'
      }, (downloadId) => {
        if (chrome.runtime.lastError) {
          console.error("Download failed:", chrome.runtime.lastError.message);
        } else {
          console.log("Download started with ID:", downloadId);
          downloadedFiles.add(filename);
        }
        
        downloadCount++;
        if (downloadCount === totalDownloads) {
          // Wait a bit longer before closing tabs
          setTimeout(() => {
            if (tabIdsToClose.length > 0) {
              closeSpecificTabs(tabIdsToClose);
            } else {
              closeImageTabs();
            }
          }, 1000);
        }
      });
    });
  }
  return true;
});

function closeSpecificTabs(tabIds) {
  console.log(`Closing specific tabs: ${tabIds}`);
  tabIds.forEach(tabId => {
    chrome.tabs.remove(tabId, () => {
      if (chrome.runtime.lastError) {
        console.log(`Tab ${tabId} already closed or doesn't exist: ${chrome.runtime.lastError.message}`);
      } else {
        console.log(`Closed tab ${tabId}`);
      }
    });
  });
}