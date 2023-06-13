$.ajaxSetup({
    headers: { "X-CSRFToken": csrfToken },
  });
  
  // Function to handle the restore password request
  function restore_password() {
    // Get the user's email address
    var email = $(".input").val();
  
    // Send an AJAX request to the server to reset the password
    $.ajax({
      url: " ",
      type: "POST",
      data: {
        email: email,
      },
      success: function (response) {
        // If the server successfully reset the password, redirect the user to the password reset confirmation page
        if (response.success) {
          window.location.replace("/password_reset/done/");
        } else {
          // If there was an error with the password reset request, display the error message to the user
          var errors = response.errors;
          $("#error-message").empty();
          for (var field in errors) {
            if (errors.hasOwnProperty(field)) {
              var errorMessages = errors[field];
              if (errorMessages.length > 0) {
                $("#error-message").prepend(errorMessages[0]);
              }
            }
          }
        }
      },
    });
  }
  
  // Add an event listener to the reset password button
  $("#reset-link-button").on("click", function (event) {
    event.preventDefault();
    // Call the restore_password function when the button is clicked
    restore_password();
  });