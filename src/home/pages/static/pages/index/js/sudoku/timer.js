export var timerInterval = null;
let startTime = null;

export function setStartTime(startTimeStr) {
  startTime = new Date(startTimeStr);

  if (isNaN(startTime)) {
    console.error("Invalid start time:", startTimeStr);
    return;
  }
}

export function startTimer() {
  if (timerInterval) clearInterval(timerInterval);
  timerInterval = setInterval(updateTimer, 1000);
}

export function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

export function updateTimer() {
  const timerElement = document.getElementById("timer");
  let now = new Date();
  let elapsed = new Date(now - startTime);
  let hours = String(elapsed.getUTCHours()).padStart(2, "0");
  let minutes = String(elapsed.getUTCMinutes()).padStart(2, "0");
  let seconds = String(elapsed.getUTCSeconds()).padStart(2, "0");
  timerElement.textContent = `${hours}:${minutes}:${seconds}`;
}
