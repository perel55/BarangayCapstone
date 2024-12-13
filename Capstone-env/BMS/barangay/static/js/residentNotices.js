document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',  // Default view is month view
        dateClick: handleDateClick,
        eventClick: handleEventClick,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth, timeGridWeek, timeGridDay'
        },
        events: function(fetchInfo, successCallback, failureCallback) {
            // Fetch the notices from the server (Django view providing JSON)
            fetch('/api/notices/')
                .then(response => response.json())
                .then(data => {
                    successCallback(data);
                })
                .catch(error => {
                    console.error('Error fetching notices:', error);
                    failureCallback(error);
                });
        },
        eventClick: function(info) {
            const { event } = info;
            const noticeId = event.extendedProps.notice_id; // Use extendedProps to access custom data
        
            // Fetch detailed notice information
            fetch(`/api/notices/${noticeId}/`)
                .then(response => response.json())
                .then(data => {
                    if (!data) {
                        alert('Notice details not found.');
                        return;
                    }
        
                    // Populate modal with fetched data
                    const noticeModal = document.getElementById('noticeModal');
                    const modalTitle = document.getElementById('modalNoticeTitle');
                    const modalDescription = document.getElementById('modalNoticeDescription');
                    const modalImage = document.getElementById('modalNoticeImage');
                    const modalStartDate = document.getElementById('modalStartDate');
                    const modalEndDate = document.getElementById('modalEndDate');
                    const modalStartTime = document.getElementById('modalStartTime');
                    const modalEndTime = document.getElementById('modalEndTime');
                    const modalNoticeType = document.getElementById('modalNoticeType');
        
                    // Update modal fields with data
                    modalTitle.innerText = data.notice_name || 'No Title';
                    modalDescription.innerText = data.notice_description || 'No Description';
                    modalStartDate.innerText = data.notice_StartDate || 'Not Provided';
                    modalEndDate.innerText = data.notice_EndDate || 'Not Provided';
                    modalStartTime.innerText = data.notice_StartTime || 'Not Provided';
                    modalEndTime.innerText = data.notice_EndTime || 'Not Provided';
                    modalNoticeType.innerText = data.notice_type || 'No Type';
        
                    if (data.notice_image) {
                        modalImage.src = data.notice_image;
                        modalImage.style.display = 'block';
                    } else {
                        modalImage.style.display = 'none';
                    }
        
                    // Show the modal
                    noticeModal.style.display = 'block';
                })
                .catch(error => {
                    console.error('Error fetching notice details:', error);
                    alert('Failed to load notice details. Please try again.');
                });
        }
        

    });

    // Initialize the calendar
    calendar.render();

    // Event Handlers
function handleDateClick(info) {
    modalScheduleOverlay.style.display = 'flex';
    scheduleDateInput.value = info.dateStr;
}

    function handleEventClick(info) {
        const { event } = info;
        const scheduleId = event.extendedProps.schedule_id;
    
        eModalScheduleOverlay.style.display = 'flex';
        document.getElementById('schedule-type').value = 'Available';
        document.getElementById('schedule-start-time').value = '';
        document.getElementById('schedule-end-time').value = '';
        document.getElementById('edit-schedule-form').action = `/schedules/edit/${scheduleId}/`;
    }

    // Close modal when clicking outside of it
    window.onclick = function(event) {
        const modal = document.getElementById('noticeModal');
        if (event.target === modal) {
            modal.style.display = "none";
        }
    }
});
