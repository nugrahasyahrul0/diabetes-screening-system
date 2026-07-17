//user-guide page
document.addEventListener("DOMContentLoaded", function() {
    const accordionButtons = document.querySelectorAll('.accordion-header');

    accordionButtons.forEach(button => {
        button.addEventListener('click', () => {
            const accordionContent = button.nextElementSibling;
            const isActive = button.classList.contains('active');

            // Opsional: Tutup semua akordeon lain yang sedang terbuka
            document.querySelectorAll('.accordion-header').forEach(otherButton => {
                otherButton.classList.remove('active');
                otherButton.nextElementSibling.style.maxHeight = null;
            });

            // Jika yang diklik sebelumnya tidak aktif, buka panelnya
            if (!isActive) {
                button.classList.add('active');
                accordionContent.style.maxHeight = accordionContent.scrollHeight + "px";
            }
        });
    });
});