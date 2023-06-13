$.ajaxSetup({
    headers: { "X-CSRFToken": csrfToken },
  });

  // Define function to handle user sign-in
  function signin_user() {
    var email = $(".input").val();
    var password = $("#password").val();
    var keep_signed_in = $("#keep-signed-in").prop("checked");

    // Send Ajax request to server to authenticate user
    $.ajax({
      url: " ",
      type: "POST",
      data: {
        email: email,
        password: password,
        keep_signed_in: keep_signed_in,
      },
      success: function (response) {
        // If authentication is successful, redirect to home page
        if (response.success) {
          window.location.replace("/");
        } else {
          // If there are errors, display them to the user
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

  // Add event listener to sign-in button
  $("#continue-with-email-button-signin").on("click", function (event) {
    event.preventDefault();
    signin_user();
  });