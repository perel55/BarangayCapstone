// Selectors for modals, buttons, and calendars
let ModalScheduleOverlay = document.getElementById('Modal-Schedule-Overlay');
let EModalScheduleOverlay = document.getElementById('EModal-Schedule-Overlay');
let scheduledate = document.getElementById('schedule-date');
let cancelsched = document.getElementById('cancel-sched');
let ecancelsched = document.getElementById('ecancel-sched');

// Calendar 1 for personal schedules
var calendarEl = document.getElementById('calendar');
var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    height: 'auto',
    events: '/api/schedules/',  // Event data for personal schedules
    initialDate: new Date(),
    hiddenDays: [0],
    eventClick: function(info) {
        const event = info.event;
        const scheduleId = event.extendedProps.schedule_id;

        EModalScheduleOverlay.style.display = "flex";
        document.getElementById('eschedule-type').value = event.extendedProps.schedule_type || "Available";
        document.getElementById('eschedule-date').value = event.extendedProps.schedule_date;

        document.getElementById('eschedule-start-time').value = event.start
            ? event.start.getHours().toString().padStart(2, '0') + ':' + event.start.getMinutes().toString().padStart(2, '0')
            : '';

        document.getElementById('eschedule-end-time').value = event.end
            ? event.end.getHours().toString().padStart(2, '0') + ':' + event.end.getMinutes().toString().padStart(2, '0')
            : '';

        document.getElementById('edit-schedule-form').action = `/schedules/edit/${scheduleId}/`;
    },
    dateClick: function(info) {
        ModalScheduleOverlay.style.display = "flex";
        scheduledate.value = info.dateStr;
    }
});

calendar.render();

// Cancel buttons for modals
cancelsched.addEventListener('click', function(event){
  event.stopPropagation();
  ModalScheduleOverlay.style.display = "none";
});

ecancelsched.addEventListener('click', function(event){
  event.stopPropagation();
  EModalScheduleOverlay.style.display = "none";
});

// Month/Year Selectors for navigation
var monthSelect = document.getElementById('monthSelect');
var yearSelect = document.getElementById('yearSelect');
var currentYear = new Date().getFullYear();
var currentMonth = new Date().getMonth();
var currentDate = new Date().getDate();

for (let year = currentYear - 5; year <= currentYear + 5; year++) {
    const option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    yearSelect.appendChild(option);
}

monthSelect.value = currentMonth;
yearSelect.value = currentYear;

function updateMonthYearSelect() {
    const currentCalendarDate = calendar.getDate();
    monthSelect.value = currentCalendarDate.getMonth();
    yearSelect.value = currentCalendarDate.getFullYear();
}

monthSelect.addEventListener('change', function () {
    const selectedMonth = parseInt(this.value);
    const selectedYear = parseInt(yearSelect.value);
    calendar.gotoDate(new Date(selectedYear, selectedMonth, currentDate));
});

yearSelect.addEventListener('change', function () {
    const selectedMonth = parseInt(monthSelect.value);
    const selectedYear = parseInt(this.value);
    calendar.gotoDate(new Date(selectedYear, selectedMonth, currentDate));
});

// Calendar 2 for reviewer schedule (announcements)
var calendarEl2 = document.getElementById('calendar2');
var calendar2 = new FullCalendar.Calendar(calendarEl2, {
    initialView: 'dayGridMonth',
    height: 'auto',
    hiddenDays: [0],
    initialDate: new Date(),
    events: '/api/announcements/',  // Event data for announcements
    eventClick: function(info) {
        const announcement = info.event.extendedProps;
        // Customize or add further functionality for announcement modal here
    }
});

calendar2.render();

// Separate month/year selectors for reviewer schedule
var monthSelect2 = document.getElementById('monthSelect2');
var yearSelect2 = document.getElementById('yearSelect2');
var currentYear2 = new Date().getFullYear();
var currentMonth2 = new Date().getMonth();
var currentDate2 = new Date().getDate();

for (let year = currentYear2 - 5; year <= currentYear2 + 5; year++) {
    const option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    yearSelect2.appendChild(option);
}

monthSelect2.value = currentMonth2;
yearSelect2.value = currentYear2;

function updateMonthYearSelect2() {
    const currentCalendarDate2 = calendar2.getDate();
    monthSelect2.value = currentCalendarDate2.getMonth();
    yearSelect2.value = currentCalendarDate2.getFullYear();
}

monthSelect2.addEventListener('change', function () {
    const selectedMonth2 = parseInt(this.value);
    const selectedYear2 = parseInt(yearSelect2.value);
    calendar2.gotoDate(new Date(selectedYear2, selectedMonth2, currentDate2));
});

yearSelect2.addEventListener('change', function () {
    const selectedMonth2 = parseInt(monthSelect2.value);
    const selectedYear2 = parseInt(this.value);
    calendar2.gotoDate(new Date(selectedYear2, selectedMonth2, currentDate2));
});

// Toggle calendar views for schedules and announcements
var MyScheduleBtn = document.getElementById('MySchedule-btn');
var Reviewerbtn = document.getElementById('Reviewer-btn');
var ReviewerSchedule = document.getElementById('Reviewer-Schedule');
var ScheduleContent = document.getElementById('Schedule-Content');

MyScheduleBtn.addEventListener('click', function(){
    ScheduleContent.style.display = "flex";
    ReviewerSchedule.style.display = "none";
    MyScheduleBtn.classList.add('active-btn2');
    Reviewerbtn.classList.remove('active-btn2');
});

Reviewerbtn.addEventListener('click', function(){
    ScheduleContent.style.display = "none";
    ReviewerSchedule.style.display = "flex";
    Reviewerbtn.classList.add('active-btn2');
    MyScheduleBtn.classList.remove('active-btn2');
});

document.addEventListener('click', function(event) {
    if (event.target === ModalScheduleOverlay) {
        ModalScheduleOverlay.style.display = "none";
    }
    if (event.target === EModalScheduleOverlay) {
        EModalScheduleOverlay.style.display = "none";
    }
});
