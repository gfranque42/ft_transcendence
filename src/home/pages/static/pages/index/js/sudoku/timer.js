export var timerInterval = null;
let startTime = null;

export function setStartTime(startTimeStr) {
    // Parse the start time from the WebSocket message
    startTime = new Date(startTimeStr);
    console.log('Parsed start time:', startTime);  // Debugging step

    // Check if the date is valid
    if (isNaN(startTime)) {
        console.error('Invalid start time:', startTimeStr);  // Log an error if the date is not valid
        return;
    }
}

export function startTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    timerInterval = setInterval(updateTimer, 1000);
}

export function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}

export function updateTimer() {
    const timerElement = document.getElementById('timer');
    let now = new Date();
    let elapsed = new Date(now - startTime);
    let hours = String(elapsed.getUTCHours()).padStart(2, '0');
    let minutes = String(elapsed.getUTCMinutes()).padStart(2, '0');
    let seconds = String(elapsed.getUTCSeconds()).padStart(2, '0');
    timerElement.textContent = `${hours}:${minutes}:${seconds}`;
}
