// Function to create a new user account and show error messages if there are any
function create_user() {
    var email = $(".input").val();
    var password1 = $("#password1").val();
    var password2 = $("#password2").val();

    $.ajax({
      url: " ", // Add URL for the backend view to create a new user
      type: "POST",
      data: {
        email: email,
        password1: password1,
        password2: password2,
      },
      success: function (response) {
        if (response.success) {
          // If the user account is successfully created, redirect to the homepage
          window.location.replace("/");
        } else {
          // If there are errors, show error messages in the error divs
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
  }


  // Attach click event listener to the "Create user" button
  $("#create-user-button").on("click", function (event) {
    event.preventDefault();
    create_user();
  });