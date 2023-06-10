  // Get the avatar and dropdown menu elements by their IDs
  const avatar = document.getElementById("user-profile-dropdown-trigger");
  const dropdownMenu = document.getElementById("user-profile-dropdown-menu");

  // Add a click event listener to the avatar element
  avatar.addEventListener("click", function () {
    // Toggle the "show" class on the dropdown menu element to show or hide it
    dropdownMenu.classList.toggle("show");
  });

  // Add a click event listener to the document object
  document.addEventListener("click", function (event) {
    // Check if the click event occurred inside the avatar or dropdown menu elements
    const isClickInside =
      avatar.contains(event.target) || dropdownMenu.contains(event.target);
    // If the click event occurred outside of the avatar or dropdown menu elements, hide the dropdown menu
    if (!isClickInside) {
      dropdownMenu.classList.remove("show");
    }
  });