
    document.addEventListener('DOMContentLoaded', () => {
        const form = document.querySelector('#addMemberModal form');
        const warningDiv = document.createElement('div');
        warningDiv.id = 'warningMessage';
        warningDiv.style.display = 'none';
        warningDiv.style.position = 'fixed';
        warningDiv.style.top = '50%';
        warningDiv.style.left = '50%';
        warningDiv.style.transform = 'translate(-50%, -50%)';
        warningDiv.style.padding = '20px';
        warningDiv.style.backgroundColor = 'rgba(255, 0, 0, 0.8)';
        warningDiv.style.color = '#fff';
        warningDiv.style.fontWeight = 'bold';
        warningDiv.style.borderRadius = '5px';
        warningDiv.style.textAlign = 'center';
        document.body.appendChild(warningDiv);

        form.addEventListener('submit', (event) => {
            event.preventDefault(); // Prevent default form submission
            const formData = new FormData(form);
            
            fetch("{% url 'member_create' household.id %}", {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    // Display blinking warning
                    warningDiv.innerText = data.error;
                    warningDiv.style.display = 'block';

                    let blink = true;
                    const blinkInterval = setInterval(() => {
                        warningDiv.style.opacity = blink ? '1' : '0.5';
                        blink = !blink;
                    }, 500);

                    setTimeout(() => {
                        clearInterval(blinkInterval);
                        warningDiv.style.display = 'none';
                    }, 5000);
                } else {
                    // Success case: reload the member list or update the UI
                    location.reload();
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

