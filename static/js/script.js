// Auto fade flash messages after 3 seconds
window.addEventListener('DOMContentLoaded', (event) => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade-out');
        }, 3000);
    });
});
