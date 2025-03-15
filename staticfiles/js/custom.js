document.addEventListener('DOMContentLoaded', function () {
    // Handle the "Log Out" button click inside the modal
    const logOutButton = document.querySelector('.btn-primary');
    if (logOutButton) {
        logOutButton.addEventListener('click', function() {
            $('#logoutModal').modal('hide');  // Hide the modal
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        ClassicEditor
            .create(document.querySelector('.ckeditor'))
            .catch(error => {
                console.error(error);
            });
    });
});
