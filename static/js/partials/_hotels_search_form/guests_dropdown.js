const guest = document.getElementById("guests"); // Get the element with the id "guests"
  const guestdropdownMenu = document.getElementById(
    "guests-input-container-dropdown-menu"
  ); // Get the element with the id "guests-input-container-dropdown-menu"

  guest.addEventListener("click", function () {
    // Add a click event listener to the "guest" element
    guestdropdownMenu.classList.toggle("show"); // Toggle the "show" class on the "guestdropdownMenu" element
    setGuests();

  });

  document.addEventListener("click", function (event) {
    // Add a click event listener to the document
    const isClickInside =
      guest.contains(event.target) || guestdropdownMenu.contains(event.target); // Check if the click event happened inside the "guest" element or the "guestdropdownMenu" element
    if (!isClickInside) {
      guestdropdownMenu.classList.remove("show"); // If the click event didn't happen inside either element, remove the "show" class from the "guestdropdownMenu" element
    }
  });