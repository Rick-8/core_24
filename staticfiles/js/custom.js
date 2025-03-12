document.addEventListener('DOMContentLoaded', function () {
    // Handle the "Log Out" button click inside the modal
    document.querySelector('.btn-primary').addEventListener('click', function() {
        $('#logoutModal').modal('hide');  // Hide the modal
    });
});
