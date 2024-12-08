// Get the modal and close button
const modal = document.getElementById("viewMoreModal");
const span = document.querySelector(".close");

// Handle the "View More" button clicks
document.querySelectorAll(".view-more-btn").forEach(button => {
    button.addEventListener("click", (event) => {
        const residentId = button.dataset.residentId;

        // Prevent the click event from propagating to the background (if clicked inside the modal)
        event.stopPropagation();

        // Fetch resident data from the backend
        fetch(`/get_resident_details/${residentId}/`)
            .then(response => response.json())
            .then(data => {
                // Inject data into modal content
                const modalContent = document.getElementById("modalContent");
                modalContent.innerHTML = `
                    ${data.picture ? `<img src="${data.picture}" alt="Resident Picture" style="max-width: 100px; max-height: 100px;"/>` : ''}
                    <p><strong>Full Name:</strong> ${data.fname} ${data.mname} ${data.lname}</p>
                    <p><strong>Username:</strong> ${data.username}</p>
                    <p><strong>Email:</strong> ${data.email}</p>
                    <p><strong>Zone:</strong> ${data.zone}</p>
                    <p><strong>Civil Status:</strong> ${data.civil_status}</p>
                    <p><strong>Occupation:</strong> ${data.occupation}</p>
                    <p><strong>Phone Number:</strong> ${data.phone_number}</p>
                     <p><strong>ID Image:</strong> ${data.id_image ? `<img src="${data.id_image}" alt="ID Image" style="max-width: 100px; max-height: 100px;"/>` : ''}</p>
                    <p><strong>Status:</strong> ${data.status}</p>
                `;
                // Show the modal
                modal.style.display = "block";
            })
            .catch(console.error);
    });
});

// Close the modal when the user clicks on <span> (x) 
span.addEventListener("click", () => modal.style.display = "none");

// Prevent the modal from closing when clicking inside the modal content
modal.querySelector(".modal-content").addEventListener("click", (event) => {
    event.stopPropagation();
});

// Close the modal when clicking outside the modal (on the background)
window.addEventListener("click", (event) => {
    if (event.target === modal) {
        modal.style.display = "none";
    }
});
