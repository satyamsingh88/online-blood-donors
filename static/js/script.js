// Dynamic animations and validation
document.addEventListener('DOMContentLoaded', () => {
    // Form Validation logic
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const phone = form.querySelector('input[name="phone"]');
            if(phone && phone.value.length < 10) {
                alert("Please enter a valid 10-digit phone number.");
                e.preventDefault();
            }
        });
    });

    // Auto-hide alert messages after 3 seconds
    const alerts = document.querySelectorAll('.alert');
    setTimeout(() => {
        alerts.forEach(a => a.style.display = 'none');
    }, 3000);
});