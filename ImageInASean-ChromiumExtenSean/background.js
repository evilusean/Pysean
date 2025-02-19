const downloadedFiles = new Set();
const DOWNLOAD_PATH = '/mnt/sdb4/MEmes/4Chan-Unsorted';

// Helper function to check if file exists in download folder
async function checkFileExists(filename) {
  try {
    // Check both the Set and the actual folder
    if (downloadedFiles.has(filename)) return true;
    
    // Check if file exists in the download folder
    const response = await fetch(`file://${DOWNLOAD_PATH}/${filename}`);
    return response.ok;
  } catch (error) {
    console.log(`Error checking file existence: ${error.message}`);
    return false;
  }
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "downloadImages") {
    console.log("Received downloadImages message with URLs:", message.urls);
    const tabsToClose = new Set();
    
    message.urls.forEach(async url => {
      const filename = url.split('/').pop();
      
      // Check for duplicates in both Set and folder
      const fileExists = await checkFileExists(filename);
      if (fileExists) {
        console.log(`Skipping duplicate image: ${filename}`);
        if (message.tabId) {
          tabsToClose.add(message.tabId);
        }
        return;
      }
      
      console.log("Downloading image:", url, "as", filename);
      chrome.downloads.download({
        url: url,
        filename: `${DOWNLOAD_PATH}/${filename}`,
        conflictAction: 'uniquify'
      }, (downloadId) => {
        if (chrome.runtime.lastError) {
          console.error("Download failed:", chrome.runtime.lastError.message);
        } else {
          console.log("Download started with ID:", downloadId);
          downloadedFiles.add(filename);
          if (message.tabId) {
            tabsToClose.add(message.tabId);
          }
        }
      });
    });

    // Close image tabs after downloads are complete
    setTimeout(() => {
      if (tabsToClose.size > 0) {
        chrome.tabs.query({ currentWindow: true }, (tabs) => {
          const imageTabIds = tabs
            .filter(tab => 
              tab.url && 
              tab.url.startsWith('https://i.4cdn.org/') && 
              (tab.url.endsWith('.jpg') || tab.url.endsWith('.png'))
            )
            .map(tab => tab.id);
          
          chrome.tabs.remove([...imageTabIds], () => {
            if (chrome.runtime.lastError) {
              console.error("Error closing tabs:", chrome.runtime.lastError.message);
            } else {
              console.log("Closed image tabs:", imageTabIds);
            }
          });
        });
      }
    }, 1000); // Wait 1 second for downloads to start
  }
  return true;
});