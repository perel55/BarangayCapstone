let allBtn = document.getElementById('all-btn');
let tbBtn = document.getElementById('tb-btn');
let immunizeBtn = document.getElementById('immunize-btn');

let allServiceArea = document.getElementById('AllService-Area');
let tbArea = document.getElementById('TB-Area');
let immunizeArea = document.getElementById('Immunize-Area');

// Set initial active button
allBtn.classList.add('active-btn');
allBtn.style.backgroundColor = "black";

let buttons = document.querySelectorAll('.Left button');
buttons.forEach(function(button) {
    button.addEventListener('click', function() {
        // Remove active class and reset styles from all buttons
        buttons.forEach(function(btn) {
            btn.classList.remove('active-btn');
            btn.style.backgroundColor = "";
        });

        // Add active class and style to the clicked button
        this.classList.add('active-btn');
        this.style.backgroundColor = 'black';

        // Hide all areas
        allServiceArea.style.display = "none";
        tbArea.style.display = "none";
        immunizeArea.style.display = "none";

        // Display the corresponding area based on the button clicked
        if (this.id === 'all-btn') {
            allServiceArea.style.display = "block";
        } else if (this.id === 'tb-btn') {
            tbArea.style.display = "block";
        } else if (this.id === 'immunize-btn') {
            immunizeArea.style.display = "block";
        }
    });
});
