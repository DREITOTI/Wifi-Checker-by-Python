const testButton = document.querySelector("#test-button");
const buttonLabel = document.querySelector("#button-label");
const statusText = document.querySelector("#status");
const statusIndicator = document.querySelector("#status-indicator");

function showStatus(message, kind = "") {
  statusText.textContent = message;
  statusIndicator.className = `status-indicator ${kind}`.trim();
}

function displayValue(id, value) {
  document.querySelector(`#${id}`).textContent =
    value === null || value === undefined ? "--" : value;
}

async function refreshStatus() {
  try {
    const response = await fetch("/api/status", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    const state = await response.json();
    displayValue("download", state.download);
    displayValue("upload", state.upload);
    displayValue("ping", state.ping);

    testButton.disabled = state.running;
    buttonLabel.textContent = state.running ? "Testing connection..." : "Test again";

    if (state.error) {
      showStatus(state.error, "error");
    } else if (state.running) {
      showStatus(state.status, "running");
    } else if (state.status === "Test complete") {
      showStatus(state.status, "success");
    } else {
      showStatus(state.status);
      buttonLabel.textContent = "Start speed test";
    }
  } catch (error) {
    testButton.disabled = true;
    showStatus("Cannot reach the Python server. Restart the app to try again.", "error");
  }
}

testButton.addEventListener("click", async () => {
  testButton.disabled = true;
  buttonLabel.textContent = "Starting test...";
  showStatus("Connecting to a speed-test server...", "running");

  try {
    const response = await fetch("/api/test", { method: "POST" });
    if (!response.ok) {
      const result = await response.json();
      throw new Error(result.error || `Server returned ${response.status}`);
    }
    await refreshStatus();
  } catch (error) {
    testButton.disabled = false;
    buttonLabel.textContent = "Try again";
    showStatus(error.message, "error");
  }
});

refreshStatus();
window.setInterval(refreshStatus, 1000);
