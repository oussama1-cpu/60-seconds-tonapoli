document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('date');
    const timeInput = document.getElementById('time');
    const reservationForm = document.getElementById('reservation-form');

    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.min = today;
    }

    if (timeInput) {
        const now = new Date();
        const nextHour = new Date(now.getTime() + 60 * 60 * 1000);
        const hours = String(nextHour.getHours()).padStart(2, '0');
        const minutes = String(nextHour.getMinutes()).padStart(2, '0');
        timeInput.value = `${hours}:${minutes}`;
    }

    if (reservationForm) {
        reservationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Thank you for your reservation! We will contact you shortly to confirm.');
            reservationForm.reset();
        });
    }
});
