// Select DOM elements
const modalScheduleOverlay = document.getElementById('Modal-Schedule-Overlay');
const eModalScheduleOverlay = document.getElementById('eModalScheduleOverlay');
const cancelSchedButton = document.getElementById('cancel-sched');
const eCancelSchedButton = document.getElementById('ecancel-sched');

// Initialize FullCalendar
const calendarEl = document.getElementById('calendar');
const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    height: 'auto',
    events: '/api/notices/', // API to fetch events
    initialDate: new Date(),
    dateClick: handleDateClick,
    eventClick: handleEventClick,
    eventContent: (arg) => renderEventContent(arg),
});

calendar.render();

/**
 * Renders custom event content for FullCalendar
 */
function renderEventContent(arg) {
    const eventContainer = document.createElement('div');
    eventContainer.style.backgroundColor = arg.event.extendedProps.color || 'transparent';
    eventContainer.style.border = arg.event.extendedProps.color ? 'none' : '2px solid black';
    eventContainer.style.borderRadius = '10px';
    eventContainer.style.display = 'flex';
    eventContainer.style.flexDirection = 'column';
    eventContainer.style.alignItems = 'center';
    eventContainer.style.justifyContent = 'center';

    const eventTitle = document.createElement('div');
    eventTitle.className = 'event-title';
    eventTitle.innerText = arg.event.title;

    const eventTime = document.createElement('div');
    eventTime.className = 'event-time';
    const startTime = arg.event.start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
    const endTime = arg.event.end
        ? arg.event.end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true })
        : 'N/A';
    eventTime.innerText = `${startTime} - ${endTime}`;

    eventContainer.append(eventTitle, eventTime);
    return { domNodes: [eventContainer] };
}

/**
 * Handles a date click for adding a new notice
 */
function handleDateClick(info) {
    modalScheduleOverlay.style.display = 'flex';
    document.getElementById('notice_StartDate').value = info.dateStr;
}

/**
 * Handles an event click for editing an existing notice
 */
function handleEventClick(info) {
    const { event } = info;
    const noticeId = event.extendedProps.notice_id;

    if (!noticeId) {
        console.error('Notice ID not found for the selected event.');
        alert('Unable to find the Notice ID for the selected event. Please try again.');
        return;
    }

    // Set modal values
    eModalScheduleOverlay.style.display = 'flex';
    document.getElementById('edit-notice-name').value = event.title;
    document.getElementById('edit-notice-description').value = event.extendedProps.description || '';
    
    // Use exact date string without changing it
    document.getElementById('edit-notice-StartDate').value = event.start.toISOString().split('T')[0];
    document.getElementById('edit-notice-EndDate').value = event.end ? event.end.toISOString().split('T')[0] : '';
    
    // Time should be set using time string from event directly (avoid automatic timezone conversion)
    document.getElementById('edit-notice-StartTime').value = event.start.toTimeString().split(' ')[0];
    document.getElementById('edit-notice-EndTime').value = event.end ? event.end.toTimeString().split(' ')[0] : '';
    document.getElementById('edit-notice-type').value = event.extendedProps.notice_type || '';

    // Dynamically set the form action URL
    document.getElementById('edit-schedule-form').setAttribute('data-notice-id', noticeId);
}

/**
 * Submits the edit notice form via fetch API
 */
document.getElementById('edit-schedule-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    const form = e.target;
    const noticeId = form.getAttribute('data-notice-id');

    if (!noticeId) {
        alert('Invalid Notice ID. Cannot proceed.');
        console.error('Notice ID is missing from the form. Ensure the event data is set properly.');
        return;
    }

    const noticeData = {
        notice_name: form['notice_name'].value,
        notice_description: form['notice_description'].value,
        notice_StartDate: form['notice_StartDate'].value,  // Keep the exact date
        notice_EndDate: form['notice_EndDate'].value || null, // Allow null
        notice_StartTime: form['notice_StartTime'].value,  // Use the form time value
        notice_EndTime: form['notice_EndTime'].value || null, // Allow null
        notice_type: form['notice_type'].value,
    };

    try {
        const response = await fetch(`/notices/edit/${noticeId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(noticeData),
        });

        if (response.ok) {
            const result = await response.json();
            if (result.success) {
                // Update event in FullCalendar
                const event = calendar.getEventById(noticeId);
                if (event) {
                    event.setProp('title', noticeData.notice_name);
                    event.setExtendedProp('description', noticeData.notice_description);
                    // Keep the date/time unchanged by using form values directly
                    event.setStart(`${noticeData.notice_StartDate}T${noticeData.notice_StartTime}`);
                    event.setEnd(
                        noticeData.notice_EndDate && noticeData.notice_EndTime
                            ? `${noticeData.notice_EndDate}T${noticeData.notice_EndTime}`
                            : null
                    );
                    event.setExtendedProp('notice_type', noticeData.notice_type);
                }
                alert('Notice updated successfully!');
                eModalScheduleOverlay.style.display = 'none';
            } else {
                alert(`Failed to update notice: ${result.error || 'Unknown error'}`);
            }
        } else {
            const errorText = await response.text();
            alert(`Server error: ${response.status} - ${errorText}`);
        }
    } catch (error) {
        console.error('Error while updating notice:', error);
        alert('Failed to update notice. Please try again later.');
    }
});


eDeleteSchedButton.addEventListener('click', async function () {
    const noticeId = eDeleteSchedButton.getAttribute('data-notice-id');

    if (!noticeId) {
        alert('Invalid Notice ID for deletion.');
        return;
    }

    const confirmation = confirm('Are you sure you want to delete this notice?');
    if (!confirmation) return;

    try {
        const response = await fetch(`/notices/delete/${noticeId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        });

        if (response.ok) {
            alert('Notice deleted successfully!');
            calendar.getEventById(noticeId)?.remove(); // Remove event from FullCalendar
            eModalScheduleOverlay.style.display = 'none'; // Close modal
        } else {
            const errorText = await response.text();
            alert(`Failed to delete notice: ${errorText}`);
        }
    } catch (error) {
        console.error('Error while deleting notice:', error);
        alert('Failed to delete notice. Please try again later.');
    }
});

/**
 * Closes the modal overlays
 */
window.addEventListener('click', (event) => {
    if (event.target === modalScheduleOverlay) modalScheduleOverlay.style.display = 'none';
    if (event.target === eModalScheduleOverlay) eModalScheduleOverlay.style.display = 'none';
});

cancelSchedButton.addEventListener('click', () => (modalScheduleOverlay.style.display = 'none'));
eCancelSchedButton.addEventListener('click', () => (eModalScheduleOverlay.style.display = 'none'));

/**
 * Utility function to get CSRF token
 */
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return decodeURIComponent(value);
    }
    return null;
}
