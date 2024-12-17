let UpdateBtn = document.getElementById('update-btn');
let CancelBtn = document.getElementById('cancel-btn');
let ModalUpdateOverlay = document.getElementById('Modal-Update-Overlay');


document.querySelectorAll('.update-btn').forEach(button => {
    button.addEventListener('click', function(event) {
        event.stopPropagation();
        const serviceId = button.getAttribute('data-id');
        const modalOverlay = document.getElementById(`Modal-Update-Overlay-${serviceId}`);
        if (modalOverlay) {
            modalOverlay.style.display = "flex";
        }
    });
});

document.querySelectorAll('.cancel-btn').forEach(button => {
    button.addEventListener('click', function(event) {
        event.stopPropagation();
        const serviceId = button.getAttribute('data-id');
        const modalOverlay = document.getElementById(`Modal-Update-Overlay-${serviceId}`);
        if (modalOverlay) {
            modalOverlay.style.display = "none";
        }
    });
});
