document.addEventListener("DOMContentLoaded", function () {
  // Handle the "Log Out" button click inside the modal
  const logoutButton = document.querySelector(".btn-primary");
  if (logoutButton) {
    logoutButton.addEventListener("click", function () {
      $("#logoutModal").modal("hide");
    });
  }

  // Handle the toggle active status switch
  const switches = document.querySelectorAll(".toggle-active");
  switches.forEach(function (switchEl) {
    switchEl.addEventListener("change", function () {
      const userId = switchEl.dataset.userId;
      const isActive = switchEl.checked;

      // Send AJAX request to update the status
      fetch(`/toggle-user-active/${userId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": "{{ csrf_token }}",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ is_active: isActive }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            switchEl.nextElementSibling.innerText = isActive
              ? "Active"
              : "Inactive";
            console.log(data.message);
          } else {
            console.error(data.message);
          }
        })
        .catch((error) => console.error("Error:", error));
    });
  });

  // Handle the delete user modal show event
  var deleteUserModal = document.getElementById("deleteUserModal");
  if (deleteUserModal) {
    deleteUserModal.addEventListener("show.bs.modal", function (event) {
      var button = event.relatedTarget;
      var userId = button.getAttribute("data-user-id");
      var form = document.getElementById("deleteUserForm");
      if (form) {
        form.action = "/staff_panel/delete_user/" + userId + "/";
      }
    });
  }

  // Initialize CKEditor for the description field
  if (document.getElementById("id_description")) {
    ClassicEditor.create(document.querySelector("#id_description")).catch(
      (error) => {
        console.error(error);
      }
    );
  }

  // Handle modal opening and set form action dynamically
  const deleteUserButtons = document.querySelectorAll(
    '[data-bs-toggle="modal"]'
  );
  deleteUserButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const userId = this.getAttribute("data-user-id");
      const deleteUserForm = document.getElementById("deleteUserForm");
      deleteUserForm.action =
        '{% url "staff_panel:delete_user" 0 %}'.slice(0, -1) + userId + "/";
    });
  });
});
