let BhwAccounts = document.getElementById('Bhw-Accounts');
let OfficialsAccounts = document.getElementById('Officials-Accounts');
let ResidentsAccounts = document.getElementById('Residents-Accounts');
let BhwAccArea = document.getElementById('BhwAcc-Area');
let OfficialsAccArea = document.getElementById('OfficialsAcc-Area');
let ResidentsAccArea = document.getElementById('ResidentsAcc-Area');

// Set initial active button
BhwAccounts.classList.add('active-btn');
BhwAccounts.style.backgroundColor = "black";




let areas = document.querySelectorAll('.Left button');
areas.forEach(function(area) {
    area.addEventListener('click', function() {
        areas.forEach(function(areabtn) {
            areabtn.classList.remove('active-btn');
            areabtn.style.backgroundColor = "";
        });

        this.classList.add('active-btn');
        this.style.backgroundColor = 'black';

        if (this.id === 'Bhw-Accounts') {
            BhwAccArea.style.display = "flex";
            OfficialsAccArea.style.display = "none";
            ResidentsAccArea.style.display = "none";
        } else if (this.id === 'Officials-Accounts') {
            BhwAccArea.style.display = "none";
            OfficialsAccArea.style.display = "flex";
            ResidentsAccArea.style.display = "none";
        } else if (this.id === 'Residents-Accounts') {
            BhwAccArea.style.display = "none";
            OfficialsAccArea.style.display = "none";
            ResidentsAccArea.style.display = "flex";
        }
    });
});
