let ModalScheduleOverlay = document.getElementById('Modal-Schedule-Overlay');
let EModalScheduleOverlay = document.getElementById('EModal-Schedule-Overlay');
let scheduledate = document.getElementById('schedule-date');
let cancelsched = document.getElementById('cancel-sched');
let ecancelsched = document.getElementById('ecancel-sched');

// Initialize FullCalendar
var calendarEl = document.getElementById('calendar');
var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth', // Set the default view to month view
    height: 'auto',
    events: '/api/schedules/', // Fetch events from the backend API
    initialDate: new Date(),  // Start on the current date
    hiddenDays: [0],  // Hide Sundays (0 is Sunday)
    dateClick: function(info) {
        // Trigger when a date is clicked
        ModalScheduleOverlay.style.display = "flex"; // Show the modal to add a new schedule
        scheduledate.value = info.dateStr;  // Set the selected date in the input field
    },
    eventClick: function(info) {
        // Trigger when an event is clicked to edit or view details
        var event = info.event;
        var scheduleId = event.extendedProps.schedule_id;

        // Show the event editing modal
        EModalScheduleOverlay.style.display = "flex";
        document.getElementById('eschedule-type').value = event.extendedProps.schedule_type || "Available";
        document.getElementById('eschedule-date').value = event.extendedProps.schedule_date;
        document.getElementById('eschedule-start-time').value = 
            event.start ? event.start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';
        document.getElementById('eschedule-end-time').value = 
            event.end ? event.end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';
        
        // Set the form action for editing the event
        document.getElementById('edit-schedule-form').action = `/schedules/edit/${scheduleId}/`;
    },
    eventContent: function(arg) {
        // Customize the event appearance (start time, end time, etc.)
        var startTime = arg.event.start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
        var endTime = arg.event.end ? arg.event.end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true }) : '';
        var scheduleTypeClass = arg.event.extendedProps.schedule_type === "Available" ? "Available" : "Not-Available";
        var scheduleId = arg.event.extendedProps.schedule_id;

        var deleteButton = document.createElement('img');
        deleteButton.className = 'delete-event';
        deleteButton.src = '../static/images/Delete-2--Streamline-Block---Free.png';
        deleteButton.dataset.scheduleId = scheduleId;

        // Event deletion handling
        deleteButton.addEventListener('click', function(event) {
            event.stopPropagation();
            deleteEvent(scheduleId);  // Call the function to delete the event
        });

        var eventContainer = document.createElement('div');
        eventContainer.className = `event-container ${scheduleTypeClass}`;

        var availabilityIndicator = document.createElement('div');
        availabilityIndicator.className = `availability-indicator ${arg.event.extendedProps.schedule_type === 'Available' ? 'green' : 'red'}`;

        var eventTime = document.createElement('div');
        eventTime.className = 'event-time';
        eventTime.innerText = `${startTime} - ${endTime}`;

        availabilityIndicator.append(eventTime);
        eventContainer.appendChild(availabilityIndicator);
        eventContainer.appendChild(deleteButton);

        return { domNodes: [eventContainer] };
    }
});

// Render the calendar
calendar.render();

// Handle modal cancel actions
cancelsched.addEventListener('click', function(event){
    event.stopPropagation();
    ModalScheduleOverlay.style.display = "none";  // Hide the modal
})

ecancelsched.addEventListener('click', function(event){
    event.stopPropagation();
    EModalScheduleOverlay.style.display = "none";  // Hide the edit modal
})

// Fetch and update events from backend using the FullCalendar API
function getEvents() {
    fetch('/api/schedules/')
        .then(response => response.json())
        .then(data => {
            calendar.addEventSource(data); // Add events to FullCalendar
        })
        .catch(error => console.error('Error fetching events:', error));
}

// Function to delete an event
function deleteEvent(scheduleId) {
    if (confirm("Are you sure you want to delete this schedule?")) {
        fetch(`/schedules/delete/${scheduleId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is sent with request
            }
        })
        .then(response => {
            if (response.ok) {
                calendar.getEventById(scheduleId).remove(); // Remove event from calendar
            } else {
                alert('Failed to delete the event');
            }
        })
        .catch(error => console.error('Error deleting event:', error));
    }
}

// Utility to get the CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Month/Year Select functionality
var monthSelect = document.getElementById('monthSelect');
var yearSelect = document.getElementById('yearSelect');
var currentYear = new Date().getFullYear();
var currentMonth = new Date().getMonth();
var currentDate = new Date().getDate();

// Populate the month and year selects
for (var year = currentYear - 5; year <= currentYear + 5; year++) {
    var option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    yearSelect.appendChild(option);
}

monthSelect.value = currentMonth;
yearSelect.value = currentYear;

// Update the calendar when the user changes month or year
monthSelect.addEventListener('change', function () {
    var selectedMonth = parseInt(this.value);
    var selectedYear = parseInt(yearSelect.value);
    calendar.gotoDate(new Date(selectedYear, selectedMonth, currentDate));  // Go to selected date
});

yearSelect.addEventListener('change', function () {
    var selectedMonth = parseInt(monthSelect.value);
    var selectedYear = parseInt(this.value);
    calendar.gotoDate(new Date(selectedYear, selectedMonth, currentDate));  // Go to selected date
});

// Calendar view button functionality (day, week, month)
var buttons = document.querySelectorAll('.SC-CalendarView button');
buttons.forEach(function(button) {
    button.addEventListener('click', function() {
        buttons.forEach(function(btn) {
            btn.classList.remove('active-btn');
            btn.style.backgroundColor = "";
        });

        this.classList.add('active-btn');
        this.style.backgroundColor = '#ffffff';

        if (this.id === 'dayView') {
            calendar.changeView('timeGridDay');
        } else if (this.id === 'weekView') {
            calendar.changeView('timeGridWeek');
        } else if (this.id === 'monthView') {
            calendar.changeView('dayGridMonth');
        }
    });
});

// Navigation buttons to move between months
document.getElementById('prevSchedule').addEventListener('click', function() {
    calendar.prev();
});

document.getElementById('nextSchedule').addEventListener('click', function() {
    calendar.next();
});

// Close modals when clicking outside
document.addEventListener('click', function(event) {
    if (event.target === ModalScheduleOverlay) {
        ModalScheduleOverlay.style.display = "none";  // Close add schedule modal
    }
    if (event.target === EModalScheduleOverlay) {
        EModalScheduleOverlay.style.display = "none";  // Close edit schedule modal
    }
});
