(async () => {
  try {
    const currentUrl = window.location.href;
    const domain = new URL(currentUrl).hostname;

    // Call local DoTask server or app logic here
    // Since reading local files isn't allowed, simulate using fetch to local server (if implemented)
    const response = await fetch('http://localhost:5678/mark', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: domain })
    });

    const result = await response.json();
    console.log("[DoTask Extension] Visit logged:", result);
  } catch (err) {
    console.error("[DoTask Extension] Error:", err);
  }
})();
