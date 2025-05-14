document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('sidebarCollapse');
    const content = document.getElementById('content');

    // Toggle sidebar
    toggleBtn.addEventListener('click', function() {
        sidebar.classList.toggle('expanded');
        content.classList.toggle('expanded');
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768 && !sidebar.contains(e.target) && 
            e.target !== toggleBtn && !toggleBtn.contains(e.target)) {
            sidebar.classList.remove('expanded');
            content.classList.remove('expanded');
        }
    });
});
