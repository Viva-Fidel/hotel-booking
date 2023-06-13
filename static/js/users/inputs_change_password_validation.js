$.ajaxSetup({
    headers: { "X-CSRFToken": csrfToken },
  });
  
  // Function to change the user's password
  function change_password() {
    // Get values from password fields
    var password1 = $('#password1').val();
    var password2 = $('#password2').val();
  
    // Send AJAX request to server with password data
    $.ajax({
      url: " ", // URL to send request to (empty string for current page URL)
      type: "POST",
      data: {
        password1: password1,
        password2: password2
      },
      success: function(response) {
        // If password change was successful, redirect to home page
        if (response.success) {
          window.location.replace("/");
        } else {
          // If there were errors, display them on the page
          var errors = response.errors;
          $("#password1-error-message").empty();
          $("#password2-error-message").empty();
          for (var field in errors) {
            if (errors.hasOwnProperty(field)) {
              var errorMessages = errors[field];
              if (errorMessages.length > 0) {
                $("#password1-error-message").prepend(errorMessages[0]);
                $("#password2-error-message").prepend(errorMessages[0]);
              }
            }
          }
        }
      },
    });
  };
  
  // Bind click event to "change password" button
  $('#change-password-button').on('click', function(event) {
    event.preventDefault();
    change_password();
  });