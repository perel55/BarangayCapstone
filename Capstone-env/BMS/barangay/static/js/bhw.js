let BhwAccounts = document.getElementById('Bhw-Accounts');
let BhwAdminAccounts = document.getElementById('BhwAdmin-Accounts');
let OfficialsAccounts = document.getElementById('Officials-Accounts');
let ResidentsAccounts = document.getElementById('Residents-Accounts');
let BsiAccounts = document.getElementById('Bsi-Accounts');

let BhwAccArea = document.getElementById('BhwAcc-Area');
let BhwAdminAccArea = document.getElementById('BhwAdminAcc-Area');
let OfficialsAccArea = document.getElementById('OfficialsAcc-Area');
let ResidentsAccArea = document.getElementById('ResidentsAcc-Area');
let BsiAccArea = document.getElementById('BsiAcc-Area');
// Set initial active button
ResidentsAccounts.classList.add('active-btn');
ResidentsAccounts.style.backgroundColor = "black";

let areas = document.querySelectorAll('.Left button');
areas.forEach(function(area) {
    area.addEventListener('click', function() {

        areas.forEach(function(areabtn) {
            areabtn.classList.remove('active-btn');
            areabtn.style.backgroundColor = "";
        });


        this.classList.add('active-btn');
        this.style.backgroundColor = 'black';

 
        if (this.id === 'Residents-Accounts') {
            ResidentsAccArea.style.display = "flex";
            BhwAccArea.style.display = "none";
            BsiAccArea.style.display = "none";
            BhwAdminAccArea.style.display = "none";
            OfficialsAccArea.style.display = "none";
        }else if (this.id === 'Bhw-Accounts'){
            BhwAccArea.style.display = "flex";
            BsiAccArea.style.display = "none";
            BhwAdminAccArea.style.display = "none";
            OfficialsAccArea.style.display = "none";
            ResidentsAccArea.style.display = "none";   
        } else if (this.id === 'Bsi-Accounts'){
            BhwAccArea.style.display = "none";
            BsiAccArea.style.display = "flex";
            BhwAdminAccArea.style.display = "none";
            OfficialsAccArea.style.display = "none";
            ResidentsAccArea.style.display = "none";
        }else if (this.id === 'BhwAdmin-Accounts') {
            BhwAccArea.style.display = "none";
            BsiAccArea.style.display = "none";
            BhwAdminAccArea.style.display = "flex";
            OfficialsAccArea.style.display = "none";
            ResidentsAccArea.style.display = "none";
        } else if (this.id === 'Officials-Accounts') {
            BhwAccArea.style.display = "none";
            BsiAccArea.style.display = "none";
            BhwAdminAccArea.style.display = "none";
            OfficialsAccArea.style.display = "flex";
            ResidentsAccArea.style.display = "none";
        } 
    });
});
