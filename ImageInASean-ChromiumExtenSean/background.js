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

// Use a direct approach to check 8kun URLs
function isValidImageUrl(url) {
  if (!url) return false;
  
  // Check for 4chan URLs
  if (url.startsWith('https://i.4cdn.org/') && 
      VALID_EXTENSIONS.some(ext => url.toLowerCase().endsWith(ext))) {
    return true;
  }
  
  // Check for 8kun/file_store URLs with detailed logging
  if (url.includes('8kun.top') && url.includes('file_store') && 
      VALID_EXTENSIONS.some(ext => url.toLowerCase().endsWith(ext))) {
    console.log(`Found valid 8kun image URL: ${url}`);
    return true;
  }
  
  return false;
}

// Function to close all image tabs
function closeImageTabs() {
  console.log("Attempting to close all image tabs...");
  
  chrome.tabs.query({ currentWindow: true }, (tabs) => {
    // Find all tabs with image URLs
    const imageTabs = tabs.filter(tab => tab.url && isValidImageUrl(tab.url));
    console.log(`Found ${imageTabs.length} image tabs to close:`, imageTabs.map(t => t.url));
    
    // Close each image tab
    imageTabs.forEach(tab => {
      chrome.tabs.remove(tab.id, () => {
        if (chrome.runtime.lastError) {
          console.error(`Error closing tab ${tab.id}:`, chrome.runtime.lastError);
        } else {
          console.log(`Successfully closed tab ${tab.id}`);
        }
      });
    });
  });
}

// Process download message
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "downloadImages") {
    console.log("Received downloadImages message:", message);
    
    // Extract the URLs and tab ID
    const urls = message.urls || [];
    const tabId = message.tabId;
    
    console.log(`Processing ${urls.length} URLs, tab ID: ${tabId}`);
    
    if (urls.length === 0) {
      console.log("No URLs to download");
      return true;
    }
    
    let downloadCount = 0;
    
    // Download each URL
    urls.forEach(url => {
      const filename = url.split('/').pop();
      
      // Skip duplicates
      if (downloadedFiles.has(filename)) {
        console.log(`Skipping duplicate: ${filename}`);
        downloadCount++;
        
        // If all downloads are complete, close tabs
        if (downloadCount === urls.length) {
          setTimeout(() => {
            if (tabId) {
              console.log(`Closing specific tab: ${tabId}`);
              chrome.tabs.remove(tabId, () => {
                if (chrome.runtime.lastError) {
                  console.error(`Error closing tab ${tabId}:`, chrome.runtime.lastError);
                } else {
                  console.log(`Successfully closed tab ${tabId}`);
                }
              });
            } else {
              closeImageTabs();
            }
          }, 1500); // Longer delay to ensure download completes
        }
        return;
      }
      
      // Download the file
      console.log(`Downloading: ${url} as ${filename}`);
      chrome.downloads.download({
        url: url,
        filename: `${DOWNLOAD_PATH}/${filename}`,
        conflictAction: 'uniquify'
      }, (downloadId) => {
        // Check for errors
        if (chrome.runtime.lastError) {
          console.error(`Download failed:`, chrome.runtime.lastError);
        } else {
          console.log(`Download started with ID: ${downloadId}`);
          downloadedFiles.add(filename);
        }
        
        // Increment counter and check if we're done
        downloadCount++;
        console.log(`Completed ${downloadCount} of ${urls.length} downloads`);
        
        // If all downloads are complete, close tabs
        if (downloadCount === urls.length) {
          setTimeout(() => {
            if (tabId) {
              console.log(`Closing specific tab: ${tabId}`);
              chrome.tabs.remove(tabId, () => {
                if (chrome.runtime.lastError) {
                  console.error(`Error closing tab ${tabId}:`, chrome.runtime.lastError);
                } else {
                  console.log(`Successfully closed tab ${tabId}`);
                }
              });
            } else {
              closeImageTabs();
            }
          }, 1500); // Longer delay to ensure download completes
        }
      });
    });
  }
  return true;
});