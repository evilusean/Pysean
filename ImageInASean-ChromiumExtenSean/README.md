# 4chan Image Saver Extension

A Chrome extension for automatically downloading images from 4chan

## Recent Updates for Ungoogled Chromium

The extension has been updated to work with Ungoogled Chromium's stricter security policies:

### Changes Made:
1. **Added `downloads.shelf` permission** - Allows automatic downloads without user prompts
2. **Added `storage` permission** - Helps with Ungoogled Chromium's security model
3. **Enhanced download logic** - Multiple fallback methods:
   - Primary: Fetch API with blob URLs
   - Fallback 1: XMLHttpRequest with blob URLs
   - Fallback 2: Direct content script download
4. **Improved error handling** - Better logging and error recovery
5. **Download monitoring** - Added download progress tracking
6. **Extended host permissions** - Added specific 8kun subdomains

### Key Features:
- Automatically downloads images from 4chan (`i.4cdn.org`) and 8kun (`8kun.top/file_store`)
- Saves images to a designated folder (`4Chan-Unsorted`)
- Closes image tabs after successful download
- Handles duplicate files automatically
- Works with Ungoogled Chromium's security model
- Multiple fallback methods ensure downloads work even with strict security

## Installation

1. Load the extension as an unpacked extension in Chrome/Ungoogled Chromium
2. Navigate to `chrome://extensions/`
3. Enable "Developer mode"
4. Click "Load unpacked" and select this folder

## Usage

1. Open image tabs from 4chan or 8kun boards
2. Click the extension icon in your browser toolbar
3. Click "Save Images" button
4. Images will be automatically downloaded to the `4Chan-Unsorted` folder
5. Image tabs will be closed after successful download

## Supported File Types

- Images: `.jpg`, `.jpeg`, `.png`, `.gif`
- Videos: `.webm`, `.mp4` (note: video downloads may not work in all cases)

## Troubleshooting for Ungoogled Chromium

If downloads still prompt for manual save:
1. **Reload the extension** after making changes
2. Check that all permissions are granted in `chrome://extensions/`
3. Ensure you're clicking the "Save Images" button (not just opening image tabs)
4. Check the browser console for any error messages
5. Verify that the image URLs are from supported hosts (`i.4cdn.org` or `8kun.top/file_store`)
6. The extension now uses multiple fallback methods - check console logs to see which method is being used

## Technical Details

The extension now uses a multi-layered approach to handle Ungoogled Chromium's restrictions:

1. **Primary Method**: Fetch API → Blob → Object URL → Download
2. **Fallback 1**: XMLHttpRequest → Blob → Object URL → Download  
3. **Fallback 2**: Content script creates download link directly

This ensures maximum compatibility with different security configurations.

## Permissions

- `activeTab` - Access to current tab
- `downloads` - Download files
- `downloads.shelf` - Automatic downloads without prompts
- `storage` - Storage access for better security handling
- `tabs` - Access to browser tabs
- `scripting` - Execute scripts in tabs
- `host_permissions` - Access to 4chan and 8kun domains 
