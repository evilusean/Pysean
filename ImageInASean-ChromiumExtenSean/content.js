function getImageUrls() {
    const images = document.querySelectorAll('img[src*=".jpg"], img[src*=".png"]');
    return Array.from(images)
      .filter(img => !img.closest('.postContainer')) // Adjust the selector based on the actual structure of 4chan posts
      .map(img => img.src);
  }
  
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "getImages") {
      const urls = getImageUrls();
      sendResponse({ urls: urls });
    }
  });
/*
TODO : Inspect 4chan post elements, so we aren't saving every image of currently
  ongoing posts, and we are ONLY saving images I've opened in seperate tabs
In this code, the getImageUrls function filters out images that are inside 
    elements with the class postContainer. You may need to adjust the selector 
    .postContainer based on the actual structure of 4chan posts. 
    Inspect the HTML structure of a 4chan post to find the appropriate class or
     element to use in the closest method.

With this change, the popup.js code you provided will now only download 
images that are not part of posts.
  */