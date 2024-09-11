export var timerInterval = null;
let startTime = null;

export function setStartTime() {
	let tmp = document.getElementById("start-time").value;
	console.log('Fetched start time:', tmp);  // Debugging step
    startTime = new Date(tmp);

    // Check if the date is valid
    if (isNaN(startTime)) {
        console.error('Invalid start time:', tmp);  // Log an error if the date is not valid
        return;
    }
    console.log('Parsed start time:', startTime);  // Debugging step
}

export function startTimer() {
    startTime = new Date(startTime);
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    timerInterval = setInterval(updateTimer, 1000);
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
