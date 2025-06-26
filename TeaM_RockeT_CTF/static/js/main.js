// Anti-cheat and security measures
(function () {
  "use strict";

  // Disable right-click and common shortcuts
  document.addEventListener("contextmenu", (e) => e.preventDefault());
  document.addEventListener("keydown", function (e) {
    // Block F12, Ctrl+Shift+I, Ctrl+U, etc.
    if (
      e.keyCode === 123 ||
      (e.ctrlKey && e.shiftKey && e.keyCode === 73) ||
      (e.ctrlKey && e.keyCode === 85) ||
      (e.ctrlKey && e.keyCode === 83)
    ) {
      e.preventDefault();
      showSecurityAlert();
      return false;
    }
  });

  // DevTools detection
  let devtools = { open: false };
  setInterval(() => {
    if (
      window.outerHeight - window.innerHeight > 160 ||
      window.outerWidth - window.innerWidth > 160
    ) {
      if (!devtools.open) {
        devtools.open = true;
        document.getElementById("security-overlay").classList.remove("hidden");
      }
    } else {
      if (devtools.open) {
        devtools.open = false;
        document.getElementById("security-overlay").classList.add("hidden");
      }
    }
  }, 1000);

  function showSecurityAlert() {
    const overlay = document.getElementById("security-overlay");
    overlay.classList.remove("hidden");
    setTimeout(() => {
      overlay.classList.add("hidden");
    }, 3000);
  }
})();

// Global state
let challengeData = null;
let currentHintLevel = 0;

// Utility functions
function showLoading() {
  document.getElementById("loading-overlay").classList.remove("hidden");
}

function hideLoading() {
  document.getElementById("loading-overlay").classList.add("hidden");
}

function updateOutput(elementId, content, isError = false) {
  const element = document.getElementById(elementId);
  if (isError) {
    element.innerHTML = `<div class="text-red-400">ERROR: ${content}</div>`;
  } else {
    element.innerHTML = content;
  }
}

// API call wrapper with error handling
async function apiCall(endpoint, data = {}) {
  try {
    showLoading();
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      if (response.status === 429) {
        throw new Error(
          "Rate limit exceeded. Please wait before trying again."
        );
      }
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    throw error;
  } finally {
    hideLoading();
  }
}

// Challenge functions
async function loadChallengeData() {
  try {
    challengeData = await apiCall("/api/challenge_data");

    // Update crypto input with encrypted data
    document.getElementById("crypto-input").value =
      challengeData.encrypted_data;

    // Display protocol samples
    let protocolOutput =
      '<div class="text-yellow-400">// INTERCEPTED PROTOCOL MESSAGES:</div>';
    challengeData.protocol_samples.forEach((sample, index) => {
      protocolOutput += `<div class="text-white mt-2">Message ${index + 1}: ${
        sample.description
      }</div>`;
      protocolOutput += `<div class="text-green-400 font-mono text-xs break-all">${sample.hex}</div>`;
    });

    updateOutput("protocol-output", protocolOutput);

    // Update intel feed
    let intelContent =
      '<div class="text-yellow-400">// MISSION INTELLIGENCE UPDATED:</div>';
    intelContent += `<div class="text-white mt-2">${challengeData.story.description}</div>`;
    intelContent += '<div class="text-cyan-400 mt-2">OBJECTIVES:</div>';
    challengeData.story.objectives.forEach((obj) => {
      intelContent += `<div class="text-gray-300">• ${obj}</div>`;
    });

    updateOutput("intel-output", intelContent);
  } catch (error) {
    updateOutput("intel-output", error.message, true);
  }
}

async function analyzeProtocol() {
  const hexInput = document.getElementById("protocol-input").value;

  if (!hexInput.trim()) {
    updateOutput("protocol-output", "Please enter hex data to analyze", true);
    return;
  }

  try {
    const result = await apiCall("/api/protocol_analyze", {
      hex_data: hexInput,
    });

    if (result.success) {
      let output =
        '<div class="text-yellow-400">// PROTOCOL ANALYSIS SUCCESSFUL:</div>';
      output += `<div class="text-white mt-2">Magic Bytes: ${result.analysis.magic_bytes}</div>`;
      output += `<div class="text-white">Pokemon ID: ${result.analysis.pokemon_id}</div>`;
      output += `<div class="text-white">Command: ${result.analysis.command}</div>`;
      output += `<div class="text-white">Payload Length: ${result.analysis.payload_length}</div>`;
      output += `<div class="text-green-400 mt-2">Decoded Payload: "${result.analysis.payload}"</div>`;

      updateOutput("protocol-output", output);
    } else {
      updateOutput("protocol-output", result.error, true);
    }
  } catch (error) {
    updateOutput("protocol-output", error.message, true);
  }
}

async function searchDatabase() {
  const query = document.getElementById("db-search-input").value;

  if (!query.trim()) {
    updateOutput("database-output", "Please enter a search query", true);
    return;
  }

  try {
    const result = await apiCall("/api/database_search", { query: query });

    let output = `<div class="text-yellow-400">// SEARCH RESULTS (${result.count} found):</div>`;

    if (result.results.length > 0) {
      result.results.forEach((pokemon) => {
        output += `<div class="text-white mt-2 border-l-2 border-blue-500 pl-2">`;
        output += `<div>ID: ${pokemon.id} | Name: ${pokemon.name}</div>`;
        output += `<div>Type: ${pokemon.type1}${
          pokemon.type2 ? "/" + pokemon.type2 : ""
        }</div>`;
        output += `<div>Access Level: ${pokemon.access_level}</div>`;
        output += `<div class="text-green-400">Secret: ${pokemon.secret_data}</div>`;
        if (pokemon.has_encrypted_payload) {
          output += `<div class="text-red-400">⚠️ Contains encrypted payload</div>`;
        }
        output += `</div>`;
      });
      output += `<div class="text-cyan-400 mt-2">💡 ${result.hint}</div>`;
    } else {
      output += '<div class="text-gray-400 mt-2">No results found</div>';
    }

    updateOutput("database-output", output);
  } catch (error) {
    updateOutput("database-output", error.message, true);
  }
}

// Cryptographic analysis functions
function frequencyAnalysis() {
  const data = document.getElementById("crypto-input").value;
  if (!data) return;

  const chars = {};
  for (let char of data) {
    chars[char] = (chars[char] || 0) + 1;
  }

  let output = '<div class="text-yellow-400">// FREQUENCY ANALYSIS:</div>';
  Object.entries(chars)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 10)
    .forEach(([char, count]) => {
      output += `<div class="text-white">'${char}': ${count} occurrences</div>`;
    });

  updateOutput("crypto-output", output);
}

function entropyCheck() {
  const data = document.getElementById("crypto-input").value;
  if (!data) return;

  const chars = {};
  for (let char of data) {
    chars[char] = (chars[char] || 0) + 1;
  }

  let entropy = 0;
  const length = data.length;

  for (let count of Object.values(chars)) {
    const p = count / length;
    entropy -= p * Math.log2(p);
  }

  let output = '<div class="text-yellow-400">// ENTROPY ANALYSIS:</div>';
  output += `<div class="text-white">Shannon Entropy: ${entropy.toFixed(
    4
  )} bits</div>`;
  output += `<div class="text-white">Data Length: ${length} bytes</div>`;

  if (entropy > 7.5) {
    output +=
      '<div class="text-green-400">High entropy - likely encrypted/compressed</div>';
  } else if (entropy > 4) {
    output +=
      '<div class="text-yellow-400">Medium entropy - possibly encoded</div>';
  } else {
    output += '<div class="text-red-400">Low entropy - likely plaintext</div>';
  }

  updateOutput("crypto-output", output);
}

function patternSearch() {
  const data = document.getElementById("crypto-input").value;
  if (!data) return;

  let output = '<div class="text-yellow-400">// PATTERN ANALYSIS:</div>';

  const patterns = new Set();
  for (let len = 2; len <= 8; len++) {
    for (let i = 0; i <= data.length - len * 2; i++) {
      const pattern = data.substr(i, len);
      if (data.indexOf(pattern, i + len) !== -1) {
        patterns.add(pattern);
      }
    }
  }

  if (patterns.size > 0) {
    output += '<div class="text-white">Repeating patterns found:</div>';
    Array.from(patterns)
      .slice(0, 5)
      .forEach((pattern) => {
        output += `<div class="text-green-400">"${pattern}"</div>`;
      });
  } else {
    output +=
      '<div class="text-gray-400">No obvious repeating patterns detected</div>';
  }

  updateOutput("crypto-output", output);
}

async function decryptAttempt() {
  const algorithm = document.getElementById("algorithm-select").value;
  const keyMaterial = document.getElementById("key-material").value;
  const encryptedData = document.getElementById("crypto-input").value;

  if (!algorithm || !keyMaterial) {
    updateOutput(
      "crypto-output",
      "Please select algorithm and provide key material",
      true
    );
    return;
  }

  try {
    const result = await apiCall("/api/decrypt_challenge", {
      algorithm: algorithm,
      key_data: keyMaterial,
      encrypted_data: encryptedData,
    });

    if (result.success) {
      document.getElementById("final-flag").textContent = result.flag;
      document.getElementById("success-modal").classList.remove("hidden");
    } else {
      updateOutput("crypto-output", result.message, true);
    }
  } catch (error) {
    updateOutput("crypto-output", error.message, true);
  }
}

async function requestHint() {
  try {
    currentHintLevel++;
    const result = await apiCall("/api/hint", { level: currentHintLevel });

    document.getElementById("intel-level").textContent = currentHintLevel;

    const intelOutput = document.getElementById("intel-output");
    intelOutput.innerHTML += `
            <div class="text-yellow-400 mt-2">// INTEL UPDATE ${currentHintLevel}:</div>
            <div class="text-blue-400">${result.hint}</div>
        `;
    intelOutput.scrollTop = intelOutput.scrollHeight;
  } catch (error) {
    updateOutput("intel-output", error.message, true);
  }
}

// Modal functions
function openSubmissionModal() {
  document.getElementById("submission-modal").classList.remove("hidden");
}

function closeSubmissionModal() {
  document.getElementById("submission-modal").classList.add("hidden");
}

function closeSuccessModal() {
  document.getElementById("success-modal").classList.add("hidden");
}

async function submitFlag() {
  const algorithm = document.getElementById("algorithm-select").value;
  const keyMaterial = document.getElementById("key-material").value;
  const flag = document.getElementById("flag-input").value;

  if (!algorithm || !keyMaterial) {
    alert("Please fill in algorithm and key material fields");
    return;
  }

  try {
    const result = await apiCall("/api/decrypt_challenge", {
      algorithm: algorithm,
      key_data: keyMaterial,
      flag: flag,
    });

    if (result.success) {
      document.getElementById("final-flag").textContent = result.flag;
      closeSubmissionModal();
      document.getElementById("success-modal").classList.remove("hidden");
    } else {
      alert(`❌ ${result.message}`);
    }
  } catch (error) {
    alert(`❌ ${error.message}`);
  }
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", function () {
  console.log(
    "%c⚠️ TEAM ROCKET SECURITY ALERT ⚠️",
    "color: red; font-size: 20px; font-weight: bold;"
  );
  console.log(
    "%cThis is a CTF challenge. Solve it properly through reverse engineering!",
    "color: yellow; font-size: 14px;"
  );

  // Auto-load challenge data after a short delay
  setTimeout(() => {
    loadChallengeData();
  }, 1000);
});
