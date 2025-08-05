let trackedWebsites = [];

// Fetch websites list from local Flask server
function fetchWebsites() {
  fetch('http://127.0.0.1:5000/websites')
    .then(response => response.json())
    .then(data => {
      trackedWebsites = data.websites || [];
      chrome.storage.local.set({trackedWebsites});
      console.log("Updated tracked websites:", trackedWebsites);
    })
    .catch(err => console.error('Failed to fetch websites:', err));
}

// Fetch once on startup
fetchWebsites();

// Refresh websites list every 30 seconds
setInterval(fetchWebsites, 30000);

// Notify Python app about visit
function notifyVisit(url) {
  fetch('http://127.0.0.1:5000/visited', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({url: url})
  })
  .then(res => res.json())
  .then(data => {
    console.log('Notified visit for', url, data);
  })
  .catch(err => console.error('Failed to notify visit:', err));
}

chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
  if (changeInfo.url) {
    for (let site of trackedWebsites) {
      if (changeInfo.url.includes(site)) {
        console.log("Visited tracked site:", site);
        notifyVisit(site);
        break; // Only notify once per URL
      }
    }
  }
});
