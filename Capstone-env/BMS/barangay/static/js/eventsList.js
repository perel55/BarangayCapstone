// Toggle between calendar and list views
let calendarButton = document.getElementById('calendar-events');
let listButton = document.getElementById('list-events');

let calendarStyle = document.getElementById('calendar-style');
let listStyle = document.getElementById('list-style');

calendarButton.addEventListener('click', function () {
    calendarStyle.style.display = 'block';
    listStyle.style.display = 'none';

    calendarButton.classList.add('active-btn');
    listButton.classList.remove('active-btn');
    calendarButton.style.backgroundColor = 'black';
    listButton.style.backgroundColor = '';
});

listButton.addEventListener('click', function () {
    calendarStyle.style.display = 'none';
    listStyle.style.display = 'block';

    listButton.classList.add('active-btn');
    calendarButton.classList.remove('active-btn');
    listButton.style.backgroundColor = 'black';
    calendarButton.style.backgroundColor = '';

    // Fetch and display events in the list format
    fetchEvents();
});

// Fetch events and display them in a list format
function fetchEvents() {
    fetch('/fetch_notices2/')  // Updated endpoint to use fetch_notices2
        .then(response => response.json())
        .then(events => {
            let eventListContainer = document.getElementById('event-list-container');
            eventListContainer.innerHTML = ''; // Clear previous content

            events.forEach(event => {
                let eventItem = document.createElement('div');
                eventItem.classList.add('event-item');

                // Event details
                eventItem.innerHTML = `
                    <h3>${event.title}</h3>
                    <p class="event-date">${formatDate(event.start)} to ${event.end ? formatDate(event.end) : 'Ongoing'}</p>
                    <p>${event.description || 'No description available.'}</p>
                `;

                eventListContainer.appendChild(eventItem);
            });
        })
        .catch(error => console.error('Error fetching events:', error));
}

// Format date to a readable format
function formatDate(date) {
    if (!date) return '';
    let d = new Date(date);
    return `${d.toLocaleDateString()} ${d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
}

// Fetch events when the page loads
window.onload = function() {
    fetchEvents();
};
