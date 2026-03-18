
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navLinks.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Smooth scrolling
    const scrollLinks = document.querySelectorAll('a[href^="#"]');
    scrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            targetElement.scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Example of dynamic content loading
    async function loadSimulationData() {
        try {
            const response = await fetch('/api/simulation/data');
            const data = await response.json();
            console.log(data);
            // Populate data into the DOM as needed
        } catch (error) {
            console.error('Error fetching simulation data:', error);
        }
    }

    loadSimulationData();
});
