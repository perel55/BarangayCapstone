let ModalScheduleOverlay = document.getElementById('Modal-Schedule-Overlay');
let EModalScheduleOverlay = document.getElementById('EModal-Schedule-Overlay');
let scheduledate = document.getElementById('schedule-date');
let cancelsched = document.getElementById('cancel-sched');
let ecancelsched = document.getElementById('ecancel-sched');

// Initialize FullCalendar
var calendarEl = document.getElementById('calendar');
var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    height: 'auto',
    events: '/api/schedules/', // Use your backend API
    initialDate: new Date(),
    hiddenDays: [0], // Optional: Hide Sundays if needed
    dateClick: function (info) {
        const selectedDate = new Date(info.dateStr);
        const today = new Date();
        today.setHours(0, 0, 0, 0); // Normalize time for accurate comparison

        if (selectedDate < today) {
            alert("You cannot schedule on a past date.");
            return; // Prevent opening the modal for past dates
        }

        // Show the scheduling modal for valid dates
        ModalScheduleOverlay.style.display = "flex";
        scheduledate.value = info.dateStr; // Set the selected date in the modal
        openScheduleModal(info.dateStr, serviceId, serviceName, servicePrice);
    },
    headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,dayGridWeek,dayGridDay',
    },
    eventClick: function (info) {
        var event = info.event;
        var scheduleId = event.id; // Event ID corresponds to the Request model ID
    
        // Show the edit modal
        EModalScheduleOverlay.style.display = "flex";
        
        // Fill in the form fields with event data
        document.getElementById('eschedule-id').value = scheduleId; // Set the request ID
        document.getElementById('eschedule-type').value = event.extendedProps.reason; // Set the reason
        document.getElementById('eschedule-date').value = event.start.toISOString().split('T')[0]; // Set the date
        document.getElementById('eschedule-start-time').value = event.start.toTimeString().split(' ')[0]; // Set start time
        document.getElementById('eschedule-price').value = event.extendedProps.total_price; // Set total price
        document.getElementById('eschedule-requirements').src = event.extendedProps.request_requirements; // Set image URL
    
        // You can also dynamically set the form action if you want
        document.getElementById('edit-schedule-form').action = `/request/edit/${scheduleId}/`; 
    },
    validRange: {
        start: null, // Allow all past and future dates to be shown
        end: null,
    },
    eventContent: function(arg) {
        // Customize the event appearance (start time, end time, etc.)
        var startTime = arg.event.start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
        var endTime = arg.event.end ? arg.event.end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true }) : '';
        var scheduleTypeClass = arg.event.extendedProps.schedule_type === "Available" ? "Available" : "Not-Available";
        var scheduleId = arg.event.extendedProps.schedule_id;

        var deleteButton = document.createElement('img');
        deleteButton.className = 'delete-event';
        deleteButton.src = '../static/images/delete.png';
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

fetch('/api/schedules/')
    .then(response => response.json())
    .then(data => {
        calendar.refetchEvents(); // Refetch events after submission
    })
    .catch(error => console.error('Error refetching events:', error));


    function deleteEvent(requestId) {
        console.log('Deleting request with ID:', requestId);  // Debug log
        if (confirm("Are you sure you want to delete this schedule?")) {
            fetch(`/schedules/delete/${requestId}/`, {  // Updated path to match the Django view
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                }
            })
            .then(response => {
                if (response.ok) {
                    console.log('Event deleted successfully.');
                    // Remove the event from the calendar
                    calendar.getEventById(requestId).remove(); 
    
                    // Show success message
                    alert('Event deleted successfully.');  // You can customize this as needed
                } else {
                    console.log('Failed to delete the event');
                    alert('Failed to delete the event');
                }
            })
            .catch(error => {
                console.error('Error deleting event:', error);
                alert('An error occurred while deleting the event');
            });
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
