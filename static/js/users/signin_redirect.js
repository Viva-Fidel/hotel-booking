// This script redirects the user to the sign-in page after 30 seconds of being on the current page.
  $(document).ready(function () {
    setTimeout(function () {
      window.location.href = "/signin/";
    }, 30000);
  });