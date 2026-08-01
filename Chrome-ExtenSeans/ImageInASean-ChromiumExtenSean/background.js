
// Service worker initialization
console.log("4chan Image Saver background script initialized");

const downloadedFiles = new Set();
const DOWNLOAD_PATH = '4Chan-Unsorted';
const VALID_EXTENSIONS = ['.jpg', '.png', '.gif', '.webm', '.mp4', '.jpeg'];

// Try to configure download behavior for Ungoogled Chromium
async function configureDownloads() {
  try {
    await chrome.storage.local.set({
      downloadPath: DOWNLOAD_PATH,
      autoDownload: true,
      skipConfirmation: true
    });

    await chrome.downloads.setUiOptions({
      useDownloadPath: true,
      createDirectory: true
    });

    console.log("Download preferences configured");
  } catch (error) {
    console.log("Could not configure download preferences:", error);
  }
}

chrome.downloads.onDeterminingFilename.addListener((item, suggest) => {
  try {
    const sourceName = (item.filename || 'download.bin').split(/[\\/]/).pop();
    const safeName = sourceName.replace(/[\\/:*?"<>|]/g, '_');
    suggest({
      filename: `${DOWNLOAD_PATH}/${safeName}`,
      conflictAction: 'uniquify'
    });
  } catch (error) {
    console.error("Could not determine download filename:", error);
    suggest({
      filename: `${DOWNLOAD_PATH}/download.bin`,
      conflictAction: 'uniquify'
    });
  }
});

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

// Small helper so batch downloads are spaced out for modern Chromium
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function startDownload(options) {
  return new Promise((resolve, reject) => {
    chrome.downloads.download(options, (downloadId) => {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
      } else {
        resolve(downloadId);
      }
    });
  });
}

// Simple download function with retry logic
async function downloadFile(url, filename, subpath = DOWNLOAD_PATH, retryCount = 0) {
  const safeFilename = filename.replace(/[\\/:*?"<>|]/g, '_').trim();
  const subpathAndFilename = `${subpath}/${safeFilename}`;
  console.log(`Downloading: ${url} as ${subpathAndFilename} (attempt ${retryCount + 1})`);
  
  if (downloadedFiles.has(subpathAndFilename)) {
    console.log(`Skipping duplicate: ${subpathAndFilename}`);
    return null;
  }
  
  try {
    const downloadId = await startDownload({
      url
    });

    console.log(`Download started with ID: ${downloadId}`);
    downloadedFiles.add(subpathAndFilename);
    return downloadId;
  } catch (error) {
    console.error(`Download failed for ${url}:`, error);
    
    if (retryCount < 2) {
      console.log(`Retrying download for ${filename} in 1 second...`);
      await delay(1000);
      return downloadFile(url, filename, subpath, retryCount + 1);
    }

    console.error(`Failed to download ${filename} after ${retryCount + 1} attempts`);
    return null;
  }
}

async function downloadBatchInQueue(urls, subpath = DOWNLOAD_PATH) {
  const results = [];

  for (let index = 0; index < urls.length; index += 1) {
    if (index > 0) {
      await delay(750);
    }

    const url = urls[index];
    const filename = decodeURIComponent((url.split('/').pop() || `image-${index + 1}`).trim());
    results.push(await downloadFile(url, filename, subpath));
  }

  return results;
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
    
    void (async () => {
      try {
        await downloadBatchInQueue(urls, DOWNLOAD_PATH);
        console.log(`Queued ${urls.length} image downloads`);

        setTimeout(() => {
          if (tabIds.length > 0) {
            console.log(`Closing ${tabIds.length} tabs after batch download`);
            closeTabs(tabIds);
          }
        }, 1500);
      } catch (error) {
        console.error("Error while downloading image batch:", error);
        setTimeout(() => {
          if (tabIds.length > 0) {
            console.log(`Closing ${tabIds.length} tabs after batch download`);
            closeTabs(tabIds);
          }
        }, 1500);
      }
    })();
  }

  // New: Download all media from a thread to a thread-specific folder
  if (message.action === "downloadThreadMedia") {
    const urls = message.urls || [];
    const threadId = message.threadId;
    if (!urls.length || !threadId) {
      console.log("No URLs or threadId for thread media download");
      return true;
    }
    void (async () => {
      try {
        await downloadBatchInQueue(urls, `4Chan-${threadId}`);
        console.log(`All thread media downloads started for thread ${threadId}`);
      } catch (error) {
        console.error(`Error while downloading thread media for ${threadId}:`, error);
      }
    })();
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