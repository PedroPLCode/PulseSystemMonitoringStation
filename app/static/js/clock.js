export function startClock(serverTimeString) {
    const serverTime = new Date(serverTimeString);
  
    if (isNaN(serverTime)) {
      console.error("Invalid server time:", serverTimeString);
      return;
    }
  
    let currentTime = new Date(serverTime.getTime());
  
    function updateClock() {
      const hours = String(currentTime.getHours()).padStart(2, '0');
      const minutes = String(currentTime.getMinutes()).padStart(2, '0');
      const seconds = String(currentTime.getSeconds()).padStart(2, '0');
      document.getElementById('clock').textContent = `${hours}:${minutes}:${seconds}`;
  
      const date = new Date();
      const shortTimezone = new Intl.DateTimeFormat("en-US", {
        timeZoneName: "short",
      }).format(date);
  
      document.getElementById('timezone').textContent = `${shortTimezone}`;
  
      currentTime.setSeconds(currentTime.getSeconds() + 1);
    }
  
    updateClock();
    setInterval(updateClock, 1000);
  }
  