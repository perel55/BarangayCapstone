let scheduleButton = document.getElementById('history-schedule');
let requestButton = document.getElementById('history-request');

// Sections to show/hide
let scheduleHistory = document.getElementById('schedule-history');
let requestHistory = document.getElementById('request-history');

// Log to check if the script is loaded correctly
console.log(scheduleButton, requestButton, scheduleHistory, requestHistory);

// Initial active button
scheduleButton.classList.add('active-btn');
scheduleButton.style.backgroundColor = 'green';

// Add click event listeners
scheduleButton.addEventListener('click', function () {
    console.log("Schedule Button Clicked");
    scheduleHistory.style.display = 'block';
    requestHistory.style.display = 'none';

    scheduleButton.classList.add('active-btn');
    requestButton.classList.remove('active-btn');
    scheduleButton.style.backgroundColor = 'green';
    requestButton.style.backgroundColor = '';
});

requestButton.addEventListener('click', function () {
    console.log("Request Button Clicked");
    requestHistory.style.display = 'block';
    scheduleHistory.style.display = 'none';

    requestButton.classList.add('active-btn');
    scheduleButton.classList.remove('active-btn');
    requestButton.style.backgroundColor = 'green';
    scheduleButton.style.backgroundColor = '';
});
