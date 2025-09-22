// Service worker initialization
console.log("4chan Image Saver background script initialized");

const downloadedFiles = new Set();
const DOWNLOAD_PATH = '4Chan-Unsorted';
const VALID_EXTENSIONS = ['.jpg', '.png', '.gif', '.webm', '.mp4', '.jpeg'];

// Try to configure download behavior for Ungoogled Chromium
async function configureDownloads() {
  try {
    // Try to set download preferences
    await chrome.storage.local.set({
      downloadPath: DOWNLOAD_PATH,
      autoDownload: true,
      skipConfirmation: true
    });
    console.log("Download preferences configured");
  } catch (error) {
    console.log("Could not configure download preferences:", error);
  }
}

// Initialize download configuration
configureDownloads();

// Use a direct approach to check 8kun URLs
function isValidImageUrl(url) {
  if (!url) return false;
  
  // Check for 4chan URLs
  if (url.startsWith('https://i.4cdn.org/') && 
      VALID_EXTENSIONS.some(ext => url.toLowerCase().endsWith(ext))) {
    return true;
  }
  
  // Check for 8kun/file_store URLs
  if (url.includes('8kun.top') && url.includes('file_store') && 
      VALID_EXTENSIONS.some(ext => url.toLowerCase().endsWith(ext))) {
    console.log(`Found valid 8kun image URL: ${url}`);
    return true;
  }
  
  return false;
}

// Function to close specific tabs
function closeTabs(tabIds) {
  console.log("Attempting to close tabs:", tabIds);
  
  tabIds.forEach(tabId => {
    chrome.tabs.remove(tabId, () => {
      if (chrome.runtime.lastError) {
        console.error(`Error closing tab ${tabId}:`, chrome.runtime.lastError);
      } else {
        console.log(`Successfully closed tab ${tabId}`);
      }
    });
  });
}

// Simple download function with retry logic
function downloadFile(url, filename, onComplete, retryCount = 0) {
  console.log(`Downloading: ${url} as ${filename} (attempt ${retryCount + 1})`);
  
  // Skip duplicates
  if (downloadedFiles.has(filename)) {
    console.log(`Skipping duplicate: ${filename}`);
    onComplete();
    return;
  }
  
  // Simple direct download approach
  chrome.downloads.download({
    url: url,
    filename: `${DOWNLOAD_PATH}/${filename}`,
    conflictAction: 'uniquify',
    saveAs: false
  }, (downloadId) => {
    if (chrome.runtime.lastError) {
      console.error(`Download failed for ${url}:`, chrome.runtime.lastError);
      
      // Retry up to 2 times with a delay
      if (retryCount < 2) {
        console.log(`Retrying download for ${filename} in 1 second...`);
        setTimeout(() => {
          downloadFile(url, filename, onComplete, retryCount + 1);
        }, 1000);
      } else {
        console.error(`Failed to download ${filename} after ${retryCount + 1} attempts`);
        onComplete();
      }
    } else {
      console.log(`Download started with ID: ${downloadId}`);
      downloadedFiles.add(filename);
      onComplete();
    }
  });
}

// Process download message
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("Message received in background script:", message);
  
  if (message.action === "downloadImages") {
    console.log("Received downloadImages message:", message);
    
    // Extract the URLs and tab IDs
    const urls = message.urls || [];
    const tabIds = message.tabIds || [];
    
    console.log(`Processing ${urls.length} URLs, tab IDs: ${tabIds}`);
    
    if (urls.length === 0) {
      console.log("No URLs to download");
      return true;
    }
    
    let downloadCount = 0;
    
    // Download each URL
    urls.forEach(url => {
      const filename = url.split('/').pop();
      
      downloadFile(url, filename, () => {
        // Increment counter and check if we're done
        downloadCount++;
        console.log(`Completed ${downloadCount} of ${urls.length} downloads`);
        
        // If all downloads are complete, close tabs
        if (downloadCount === urls.length) {
          setTimeout(() => {
            if (tabIds.length > 0) {
              console.log(`Closing ${tabIds.length} tabs after batch download`);
              closeTabs(tabIds);
            }
          }, 1500);
        }
      });
    });
  }

  // New: Download all media from a thread to a thread-specific folder
  if (message.action === "downloadThreadMedia") {
    const urls = message.urls || [];
    const threadId = message.threadId;
    if (!urls.length || !threadId) {
      console.log("No URLs or threadId for thread media download");
      return true;
    }
    let downloadCount = 0;
    urls.forEach(url => {
      const filename = url.split('/').pop();
      chrome.downloads.download({
        url: url,
        filename: `4Chan-${threadId}/${filename}`,
        conflictAction: 'uniquify',
        saveAs: false
      }, (downloadId) => {
        if (chrome.runtime.lastError) {
          console.error(`Thread download failed for ${url}:`, chrome.runtime.lastError);
        } else {
          console.log(`Thread download started with ID: ${downloadId}`);
        }
        downloadCount++;
        if (downloadCount === urls.length) {
          console.log(`All thread media downloads started for thread ${threadId}`);
        }
      });
    });
    return true;
  }
});

// Monitor download progress
chrome.downloads.onChanged.addListener((downloadDelta) => {
  if (downloadDelta.state) {
    console.log(`Download ${downloadDelta.id} state changed to: ${downloadDelta.state.current}`);
    
    if (downloadDelta.state.current === 'complete') {
      console.log(`Download ${downloadDelta.id} completed successfully`);
    } else if (downloadDelta.state.current === 'interrupted') {
      console.error(`Download ${downloadDelta.id} was interrupted`);
    }
  }
  
  if (downloadDelta.error) {
    console.error(`Download ${downloadDelta.id} error:`, downloadDelta.error.current);
  }
});