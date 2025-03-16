document.addEventListener('DOMContentLoaded', function () {
    // Handle the "Log Out" button click inside the modal
    document.querySelector('.btn-primary').addEventListener('click', function() {
        $('#logoutModal').modal('hide');  // Hide the modal
    });    
});

document.addEventListener('DOMContentLoaded', function() {
    const switches = document.querySelectorAll('.toggle-active');
    
    switches.forEach(function(switchEl) {
        switchEl.addEventListener('change', function() {
            const userId = switchEl.dataset.userId;
            const isActive = switchEl.checked;

            // Send AJAX request to update the status
            fetch(`/toggle-user-active/${userId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ is_active: isActive })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    // Optionally update the label text or show a success message
                    switchEl.nextElementSibling.innerText = isActive ? 'Active' : 'Inactive';
                    console.log(data.message);
                } else {
                    console.error(data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    var deleteUserModal = document.getElementById("deleteUserModal");
    deleteUserModal.addEventListener("show.bs.modal", function (event) {
        var button = event.relatedTarget;
        var userId = button.getAttribute("data-user-id");
        var form = document.getElementById("deleteUserForm");
        form.action = "/staff_panel/delete_user/" + userId + "/";
  // Ensure it matches your URL pattern
    });
});

