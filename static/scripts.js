// Confirmation before deleting an expense
function confirmDeletion(event) {
    if (!confirm("Are you sure you want to delete this expense?")) {
        event.preventDefault();
    }
}

// Add event listeners to all delete links
document.addEventListener("DOMContentLoaded", function () {
    const deleteLinks = document.querySelectorAll('a[data-delete]');
    deleteLinks.forEach(link => {
        link.addEventListener('click', confirmDeletion);
    });
});



