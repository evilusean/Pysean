
// Service worker initialization
console.log("[background] 4chan Image Saver background script initialized");

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

    console.log("[background] Download preferences configured");
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
    const downloadOptions = {
      ...options,
      saveAs: false,
      conflictAction: 'uniquify'
    };

    console.log('[background] Calling chrome.downloads.download with options:', downloadOptions);
    chrome.downloads.download(downloadOptions, (downloadId) => {
      console.log('[background] chrome.downloads.download callback fired with downloadId:', downloadId);
      if (chrome.runtime.lastError) {
        console.error('[background] chrome.downloads.download reported runtime error:', chrome.runtime.lastError.message);
        reject(new Error(chrome.runtime.lastError.message));
      } else {
        console.log('[background] chrome.downloads.download accepted request');
        resolve(downloadId);
      }
    });
  });
}

// Simple download function with retry logic
async function downloadFile(url, filename, subpath = DOWNLOAD_PATH, retryCount = 0) {
  const safeFilename = filename.replace(/[\\/:*?"<>|]/g, '_').trim();
  const subpathAndFilename = `${subpath}/${safeFilename}`;
  console.log(`[background] Downloading: ${url} as ${subpathAndFilename} (attempt ${retryCount + 1})`);
  
  if (downloadedFiles.has(subpathAndFilename)) {
    console.log(`[background] Skipping duplicate: ${subpathAndFilename}`);
    return null;
  }
  
  try {
    console.log(`[background] Invoking chrome.downloads.download for ${url}`);
    const downloadId = await startDownload({
      url,
      filename: subpathAndFilename
    });

    console.log(`[background] Download started with ID: ${downloadId}`);
    downloadedFiles.add(subpathAndFilename);
    return downloadId;
  } catch (error) {
    console.error(`[background] Download failed for ${url}:`, error);
    return null;
  }
}

async function downloadBatchInQueue(urls, subpath = DOWNLOAD_PATH) {
  const results = [];

  for (let index = 0; index < urls.length; index += 1) {
    const url = urls[index];
    const filename = decodeURIComponent((url.split('/').pop() || `image-${index + 1}`).trim());
    results.push(await downloadFile(url, filename, subpath));
    if (index < urls.length - 1) {
      await delay(250);
    }
  }

  return results;
}

// Process download message
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("[background] Message received in background script:", message);
  
  if (message.action === "downloadImages") {
    console.log("[background] Received downloadImages message:", message);
    
    const urls = message.urls || [];
    const tabIds = message.tabIds || [];
    
    console.log(`[background] Processing ${urls.length} URLs, tab IDs: ${tabIds}`);
    
    if (urls.length === 0) {
      console.log("No URLs to download");
      sendResponse({ ok: true });
      return true;
    }
    
    void (async () => {
      try {
        await downloadBatchInQueue(urls, DOWNLOAD_PATH);
        console.log(`[background] Queued ${urls.length} image downloads`);

        setTimeout(() => {
          if (tabIds.length > 0) {
            console.log(`Closing ${tabIds.length} tabs after batch download`);
            closeTabs(tabIds);
          }
        }, 10000);
      } catch (error) {
        console.error("[background] Error while downloading image batch:", error);
        setTimeout(() => {
          if (tabIds.length > 0) {
            console.log(`Closing ${tabIds.length} tabs after batch download`);
            closeTabs(tabIds);
          }
        }, 10000);
      }
    })();

    sendResponse({ ok: true });
    return true;
  }

  if (message.action === "downloadThreadMedia") {
    const urls = message.urls || [];
    const threadId = message.threadId;
    if (!urls.length || !threadId) {
      console.log("No URLs or threadId for thread media download");
      sendResponse({ ok: true });
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

    sendResponse({ ok: true });
    return true;
  }

  sendResponse({ ok: true });
  return true;
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