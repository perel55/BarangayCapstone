function toggleVisitFields() {
    // Get the selected vaccine
    const selectedVaccine = document.getElementById('vaccine_name').value;

    // Get the visit field elements
    const firstVisitField = document.getElementById('first-visit-field');
    const secondVisitField = document.getElementById('second-visit-field');
    const thirdVisitField = document.getElementById('third-visit-field');
    const fourthVisitField = document.getElementById('fourth-visit-field');
    const fifthVisitField = document.getElementById('fifth-visit-field');

    // Hide all fields by default
    firstVisitField.style.display = 'none';
    secondVisitField.style.display = 'none';
    thirdVisitField.style.display = 'none';
    fourthVisitField.style.display = 'none';
    fifthVisitField.style.display = 'none';

    // Display fields based on the selected vaccine
    if (
        selectedVaccine === 'Pentavalent Vaccine' ||
        selectedVaccine === 'Oral Polio Vaccine (OPV)' ||
        selectedVaccine === 'Pneumococcal Conjugate Vaccine'
    ) {
        firstVisitField.style.display = 'block';
        secondVisitField.style.display = 'block';
        thirdVisitField.style.display = 'block';
    } else if (selectedVaccine === 'Inactivated Polio Vaccine') {
        thirdVisitField.style.display = 'block';
        fourthVisitField.style.display = 'block';
    } else if (selectedVaccine === 'Measles, Mumps, Rubella') {
        fourthVisitField.style.display = 'block';
        fifthVisitField.style.display = 'block';
    }
}

// Initialize the visibility on page load
document.addEventListener('DOMContentLoaded', toggleVisitFields);

// Add an event listener for when the vaccine name changes
document.getElementById('vaccine_name').addEventListener('change', toggleVisitFields);
