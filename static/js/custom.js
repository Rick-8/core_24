document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript is running!");

    // Background Image Setup
    const bgElements = document.querySelectorAll('.background-image');

    bgElements.forEach((bgElement) => {
        const imgUrl = bgElement.getAttribute('data-bg');
        if (imgUrl) {
            bgElement.style.backgroundImage = `url("${imgUrl}")`;
            bgElement.style.backgroundSize = 'cover';
            bgElement.style.backgroundPosition = 'center';
            bgElement.style.backgroundRepeat = 'no-repeat';
        } else {
            console.error("Background image URL is missing.");
        }
    });

    // DELETE USER MODAL
    const deleteUserModal = document.getElementById("deleteUserModal");
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

    // DELETE MEMBERSHIP MODAL
    const deleteMembershipModal = document.getElementById("deleteMembershipModal");
    if (deleteMembershipModal) {
        deleteMembershipModal.addEventListener("show.bs.modal", function (event) {
            let button = event.relatedTarget;
            let membershipId = button.getAttribute("data-membership-id");
            let form = document.getElementById("deleteMembershipForm");

            if (membershipId) {
                form.action = `/join-up/memberships/delete/${membershipId}/`;
            } else {
                console.error("Membership ID is missing.");
            }
        });
    }

    // GET CSRF TOKEN FUNCTION
    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie) {
            document.cookie.split(";").forEach((cookie) => {
                let trimmedCookie = cookie.trim();
                if (trimmedCookie.startsWith("csrftoken=")) {
                    cookieValue = trimmedCookie.substring("csrftoken=".length);
                }
            });
        }
        return cookieValue;
    }

    // TOGGLE USER ACTIVE STATUS
    const switches = document.querySelectorAll(".toggle-active");
    switches.forEach((switchEl) => {
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

    // INIT CKEDITOR
    if (document.getElementById("id_description")) {
        ClassicEditor.create(document.querySelector("#id_description")).catch((error) => {
            console.error(error);
        });
    }

    // SEARCH FUNCTION
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

    // AUTO HIDE ALERT MESSAGES
    setTimeout(() => {
        document.querySelectorAll(".alert").forEach(alert => {
            alert.style.display = "none";
        });
    }, 5000);

    // SESSION TIMEOUT HANDLER
    (function setupSessionTimeout() {
        var timeoutLimit = 180000; // 3 minutes
        var logoutUrl = "/accounts/logout/";
        var timeoutWarningTimer, timeoutLogoutTimer;

        function showTimeoutModal() {
            var sessionTimeoutModal = new bootstrap.Modal(document.getElementById('sessionTimeoutModal'));
            sessionTimeoutModal.show();
        }

        function handleModalAction(isLoggedOut) {
            if (isLoggedOut) {
                window.location.href = logoutUrl;
            } else {
                resetTimers();
                var sessionTimeoutModal = bootstrap.Modal.getInstance(document.getElementById('sessionTimeoutModal'));
                sessionTimeoutModal.hide();
            }
        }

        document.getElementById('logoutButton').addEventListener('click', function () {
            handleModalAction(true);
        });

        function resetTimers() {
            clearTimeout(timeoutWarningTimer);
            clearTimeout(timeoutLogoutTimer);
            timeoutWarningTimer = setTimeout(showTimeoutModal, timeoutLimit - 60000);
            timeoutLogoutTimer = setTimeout(() => handleModalAction(true), timeoutLimit);
        }

        ['mousemove', 'keydown', 'click', 'scroll'].forEach((event) => {
            window.addEventListener(event, resetTimers);
        });

        resetTimers();
    })();
});
