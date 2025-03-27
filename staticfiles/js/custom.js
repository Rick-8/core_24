document.addEventListener("DOMContentLoaded", function () {
  // Handle delete user modal show event
  var deleteUserModal = document.getElementById("deleteUserModal");
  if (deleteUserModal) {
      deleteUserModal.addEventListener("show.bs.modal", function (event) {
          var button = event.relatedTarget;
          var userId = button.getAttribute("data-user-id");
          var form = document.getElementById("deleteUserForm");

          if (form && userId) {
              form.action = "/staff_panel/delete-user/" + userId + "/";
          }
      });
  }

  // Handle the toggle active status switch (Fixing CSRF issue)
  function getCSRFToken() {
      let cookieValue = null;
      if (document.cookie) {
          const cookies = document.cookie.split(";");
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              if (cookie.startsWith("csrftoken=")) {
                  cookieValue = cookie.substring("csrftoken=".length, cookie.length);
                  break;
              }
          }
      }
      return cookieValue;
  }

  const switches = document.querySelectorAll(".toggle-active");
  switches.forEach(function (switchEl) {
      switchEl.addEventListener("change", function () {
          const userId = switchEl.dataset.userId;
          const isActive = switchEl.checked;
          const csrfToken = getCSRFToken();

          fetch(`/staff_panel/toggle-user-active/${userId}/`, {
              method: "POST",
              headers: {
                  "X-CSRFToken": csrfToken,
                  "Content-Type": "application/json",
              },
              body: JSON.stringify({ is_active: isActive }),
          })
              .then((response) => response.json())
              .then((data) => {
                  if (data.status === "success") {
                      switchEl.nextElementSibling.innerText = isActive ? "Active" : "Inactive";
                      console.log(data.message);
                  } else {
                      console.error(data.message);
                  }
              })
              .catch((error) => console.error("Error:", error));
      });
  });

  // Initialize CKEditor where needed.
  if (document.getElementById("id_description")) {
      ClassicEditor.create(document.querySelector("#id_description")).catch((error) => {
          console.error(error);
      });
  }

  // Perform the search using fetch (AJAX)
  function performSearch() {
      var query = document.getElementById('searchInput').value;
      var csrfToken = getCSRFToken();

      fetch('/search-endpoint/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({ query: query })
      })
          .then(response => response.json())
          .then(data => {
              updateSearchResults(data.results);
          })
          .catch(error => console.error('Error performing search:', error));
  }

  // Update the UI with search results
  function updateSearchResults(results) {
      var resultsContainer = document.getElementById('resultsContainer');
      resultsContainer.innerHTML = '';


      results.forEach(function (result) {
          var resultItem = document.createElement('div');
          resultItem.classList.add('result-item');
          resultItem.textContent = result.name;
          resultsContainer.appendChild(resultItem);
      });
  }

  // Auto-hide alert message
  setTimeout(function () {
      let alerts = document.querySelectorAll(".alert");
      alerts.forEach(alert => {
          alert.style.display = "none";
      });
  }, 5000);
});
