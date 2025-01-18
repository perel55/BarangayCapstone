let OutbreakBTN = document.getElementById('Outbreak-btn');
let OutbreakArea = document.getElementById('Outbreak-area');
let OpenModalBTN = document.getElementById('openModalButton');

let TotalCasesBTN = document.getElementById('totalCases-btn');
let CasesArea = document.getElementById('Cases-area');

// Set initial active button
OutbreakBTN.classList.add('active-btn');
OutbreakBTN.style.backgroundColor = "black";

// Function to display Outbreak Area and set active button
function showOutbreakArea() {
    OutbreakArea.style.display = 'block';
    OpenModalBTN.style.display = 'block';
    CasesArea.style.display = 'none';
    
    OutbreakBTN.classList.add('active-btn');
    TotalCasesBTN.classList.remove('active-btn');
    
    OutbreakBTN.style.backgroundColor = 'black';
    TotalCasesBTN.style.backgroundColor = '';
}

// Function to display Cases Area and set active button
function showCasesArea() {
    CasesArea.style.display = 'block';
    OutbreakArea.style.display = 'none';
    OpenModalBTN.style.display = 'none';
    
    TotalCasesBTN.classList.add('active-btn');
    OutbreakBTN.classList.remove('active-btn');
    
    TotalCasesBTN.style.backgroundColor = 'black';
    OutbreakBTN.style.backgroundColor = '';
}

// Event listeners for buttons
OutbreakBTN.addEventListener('click', showOutbreakArea);
TotalCasesBTN.addEventListener('click', showCasesArea);
