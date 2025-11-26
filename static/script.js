document.getElementById('predictionForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const voltage = parseFloat(document.getElementById('voltage').value);
    const current = parseFloat(document.getElementById('current').value);
    const temperature = parseFloat(document.getElementById('temperature').value);
    const cycle = parseFloat(document.getElementById('cycle').value);

    const resultContainer = document.getElementById('resultContainer');
    const loading = document.getElementById('loading');
    const sohValue = document.getElementById('sohValue');
    const healthMessage = document.getElementById('healthMessage');
    const progressBar = document.getElementById('progressBar');

    // Show loading, hide result
    resultContainer.classList.add('hidden');
    loading.classList.remove('hidden');

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                voltage: voltage,
                current: current,
                temperature: temperature,
                cycle: cycle
            }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        const soh = data.soh;

        // Update UI
        sohValue.textContent = soh.toFixed(1);
        progressBar.style.width = `${Math.min(soh, 100)}%`;

        if (soh >= 80) {
            healthMessage.textContent = "Battery is in Good Condition";
            healthMessage.style.color = "var(--success-color)";
            progressBar.style.backgroundColor = "var(--success-color)";
        } else if (soh >= 60) {
            healthMessage.textContent = "Battery Degradation Detected";
            healthMessage.style.color = "var(--warning-color)";
            progressBar.style.backgroundColor = "var(--warning-color)";
        } else {
            healthMessage.textContent = "Battery Replacement Recommended";
            healthMessage.style.color = "var(--danger-color)";
            progressBar.style.backgroundColor = "var(--danger-color)";
        }

        loading.classList.add('hidden');
        resultContainer.classList.remove('hidden');

    } catch (error) {
        console.error('Error:', error);
        loading.classList.add('hidden');
        alert('Failed to get prediction. Ensure the backend server is running.');
    }
});

document.getElementById('predictionForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const voltage = parseFloat(document.getElementById('voltage').value);
    const current = parseFloat(document.getElementById('current').value);
    const temperature = parseFloat(document.getElementById('temperature').value);
    const cycle = parseFloat(document.getElementById('cycle').value);

    const resultContainer = document.getElementById('resultContainer');
    const loading = document.getElementById('loading');
    const sohValue = document.getElementById('sohValue');
    const healthMessage = document.getElementById('healthMessage');
    const progressBar = document.getElementById('progressBar');

    // Show loading, hide result
    resultContainer.classList.add('hidden');
    loading.classList.remove('hidden');

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                voltage: voltage,
                current: current,
                temperature: temperature,
                cycle: cycle
            }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        const soh = data.soh;

        // Update UI
        sohValue.textContent = soh.toFixed(1);
        progressBar.style.width = `${Math.min(soh, 100)}%`;

        if (soh >= 80) {
            healthMessage.textContent = "Battery is in Good Condition";
            healthMessage.style.color = "var(--success-color)";
            progressBar.style.backgroundColor = "var(--success-color)";
        } else if (soh >= 60) {
            healthMessage.textContent = "Battery Degradation Detected";
            healthMessage.style.color = "var(--warning-color)";
            progressBar.style.backgroundColor = "var(--warning-color)";
        } else {
            healthMessage.textContent = "Battery Replacement Recommended";
            healthMessage.style.color = "var(--danger-color)";
            progressBar.style.backgroundColor = "var(--danger-color)";
        }

        loading.classList.add('hidden');
        resultContainer.classList.remove('hidden');

    } catch (error) {
        console.error('Error:', error);
        loading.classList.add('hidden');
        alert('Failed to get prediction. Ensure the backend server is running.');
    }
});

// --- Live Monitor Logic ---
async function updateLiveMonitor() {
    try {
        const response = await fetch('http://127.0.0.1:5000/status');
        if (response.ok) {
            const data = await response.json();

            if (data.timestamp) {
                updateDisplay(data.voltage, data.current, data.temperature, data.cycle, data.soh);
                return;
            }
        }
        throw new Error("No data");
    } catch (error) {
        // Fallback: Generate random values for demo purposes
        const randomVoltage = 3.0 + Math.random() * 1.2;
        const randomCurrent = -2.0 + Math.random() * 1.5;
        const randomTemp = 20 + Math.random() * 15;
        const randomCycle = Math.floor(Math.random() * 200);
        // Simple linear approximation for SoH
        const randomSoH = 100 - (randomCycle * 0.05) - (Math.random() * 5);

        updateDisplay(randomVoltage, randomCurrent, randomTemp, randomCycle, randomSoH);
    }
}

function updateDisplay(voltage, current, temp, cycle, soh) {
    document.getElementById('liveVoltage').textContent = voltage.toFixed(3);
    document.getElementById('liveCurrent').textContent = current.toFixed(3);
    document.getElementById('liveTemp').textContent = temp.toFixed(1);
    document.getElementById('liveCycle').textContent = cycle;

    const liveSoH = document.getElementById('liveSoH');
    liveSoH.textContent = soh.toFixed(1);

    // Color coding for live SoH
    if (soh >= 80) liveSoH.style.color = "var(--success-color)";
    else if (soh >= 60) liveSoH.style.color = "var(--warning-color)";
    else liveSoH.style.color = "var(--danger-color)";
}

// Poll every 5 seconds
setInterval(updateLiveMonitor, 5000);
// Initial call
updateLiveMonitor();
