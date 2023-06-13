$.ajaxSetup({
  headers: { "X-CSRFToken": csrfToken },
});

// Function to validate user email and show/hide password creation form
function validate_email() {
  $.ajax({
    url: " ", // Add URL for the backend view to validate email
    type: "POST",
    data: { email: $(".input").val() }, // Send the user input email

    success: function (response) {
      if (response.success) {
        // If the email is valid, hide email form and show password form
        var email = $(".input").val();
        $(".registration-form__email").hide();
        $(".registration-form__password").show();
      } else {
        // If the email is invalid, show error messages in the error div
        var errors = response.errors;
        $("#email-error-message").empty();
        for (var field in errors) {
          if (errors.hasOwnProperty(field)) {
            var errorMessages = errors[field];
            if (errorMessages.length > 0) {
              $("#email-error-message").prepend(errorMessages[0]);
            }
          }
        }
      }
    },
  });
}

// Attach click event listener to the "Continue with email" button
$("#continue-with-email-button-registration").on("click", function (event) {
  event.preventDefault();
  validate_email();
});
