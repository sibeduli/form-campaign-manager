document.addEventListener('DOMContentLoaded', function () {
    var themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
    var themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');

    // Change the icons inside the button based on previous settings
    if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        themeToggleLightIcon.classList.remove('hidden');
        document.documentElement.classList.add('dark');
        document.documentElement.classList.remove('light');
        localStorage.setItem('color-theme', 'dark');
    } else {
        themeToggleDarkIcon.classList.remove('hidden');
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
        localStorage.setItem('color-theme', 'light');
    }

    var themeToggleBtn = document.getElementById('theme-toggle');

    themeToggleBtn.addEventListener('click', function () {
        console.log('click');

        // toggle icons inside button
        themeToggleDarkIcon.classList.toggle('hidden');
        themeToggleLightIcon.classList.toggle('hidden');

        // if set via local storage previously
        if (localStorage.getItem('color-theme')) {
            if (localStorage.getItem('color-theme') === 'light') {
                document.documentElement.classList.add('dark');
                document.documentElement.classList.remove('light');
                localStorage.setItem('color-theme', 'dark');
            } else {
                document.documentElement.classList.remove('dark');
                document.documentElement.classList.add('light');
                localStorage.setItem('color-theme', 'light');
            }

            // if NOT set via local storage previously
        } else {
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
            } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
            }
        }

    });
    function updateClock() {
        const now = new Date();
        const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        const dayName = days[now.getDay()]; // Get the name of the day
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0'); // Months are zero-based
        const day = String(now.getDate()).padStart(2, '0');

        // Format for date and time display with day name
        const dateTimeFormat = `${dayName}, ${day}/${month}/${year}, ${hours}:${minutes}:${seconds} (GMT +7)`;

        document.getElementById('clock').textContent = dateTimeFormat;
    }

    // Update the clock every second
    setInterval(updateClock, 1000);
    updateClock(); // Initialize clock immediately on page load

    // Server status handling
    function updateServerStatus(isOnline) {
        const statusText = document.getElementById('server-status-text');
        const onlinePing = document.getElementById('server-status-ping-online');
        const onlineDot = document.getElementById('server-status-dot-online');
        const offlinePing = document.getElementById('server-status-ping-offline');
        const offlineDot = document.getElementById('server-status-dot-offline');

        if (isOnline) {
            statusText.textContent = 'Server Online';
            onlinePing.classList.remove('hidden');
            onlineDot.classList.remove('hidden');
            offlinePing.classList.add('hidden');
            offlineDot.classList.add('hidden');
        } else {
            statusText.textContent = 'Server Disconnected';
            onlinePing.classList.add('hidden');
            onlineDot.classList.add('hidden');
            offlinePing.classList.remove('hidden');
            offlineDot.classList.remove('hidden');
        }
    }

    // Initialize as disconnected
    updateServerStatus(false);

    // Setup EventSource for server status
    function setupEventSource() {
        const eventSource = new EventSource('/api/server-status');
        
        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);
            updateServerStatus(data.status === 'online');
        };

        eventSource.onerror = function() {
            updateServerStatus(false);
            eventSource.close();
            // Try to reconnect after 5 seconds
            setTimeout(setupEventSource, 5000);
        };

        return eventSource;
    }

    // Initial setup
    let eventSource = setupEventSource();
});