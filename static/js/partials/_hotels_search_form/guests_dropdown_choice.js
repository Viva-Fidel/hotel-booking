function changeCount(type, operation) {
  // Get the HTML element of the count
  var countEl = document.getElementById(type + "-count");
  // Parse the current count as an integer
  var count = parseInt(countEl.innerHTML);
  // Get the minus and plus buttons for the current type
  var minusButton = document.querySelector(
    `button.guests-drop-down-menu__button_minus[onclick="changeCount('${type}', 'minus')"]`
  );
  var plusButton = document.querySelector(
    `button.guests-drop-down-menu__button_plus[onclick="changeCount('${type}', 'plus')"]`
  );

  // Decrease the count if operation is minus and count is greater than zero
  if (operation === "minus") {
    if (count > 0) {
      count--;
    }
  }
  // Increase the count if operation is plus and count is less than 30
  else if (operation === "plus") {
    if (count < 30) {
      count++;
    }
  }

  // Update the count in the HTML element
  countEl.innerHTML = count;
  // Call the setGuests() function to update the guest count in the input field
  setGuests();

  // Disable the minus button if the count is at its minimum value
  if (type === "adults" && count === 1) {
    minusButton.disabled = true;
  } else if (type === "children" && count === 0) {
    minusButton.disabled = true;
  } else if (type === "rooms" && count === 1) {
    minusButton.disabled = true;
  } else {
    minusButton.disabled = false;
  }

  // Disable the plus button if the count is at its maximum value
  if (count === 30) {
    plusButton.disabled = true;
  } else {
    plusButton.disabled = false;
  }
}

// Event listener for the search button click
document
  .getElementsByClassName("hotel-search-form__submit-buttonn")[0]
  .addEventListener("click", function (event) {
    // Get the guest count values
    var adults = parseInt(document.getElementById("adults-count").textContent);
    var children = parseInt(
      document.getElementById("children-count").textContent
    );
    var rooms = parseInt(document.getElementById("rooms-count").textContent);

    if (adults === 1 && children === 0 && rooms === 1) {
      var totalGuests = parseInt(adults) + parseInt(children);
      var guestsLabel = " guest";
      var roomsLabel = " room";

      document.getElementById("guests").value =
        totalGuests + guestsLabel + " · " + rooms + roomsLabel;
    }
  });

// Function to set the guest count in the input field
function setGuests() {
  // Get the count of adults, children, and rooms
  var adults = document.getElementById("adults-count").textContent;
  var children = document.getElementById("children-count").textContent;
  var rooms = document.getElementById("rooms-count").textContent;
  // Calculate the total number of guests
  var totalGuests = parseInt(adults) + parseInt(children);
  // Set the label for guests depending on whether there is one guest or multiple guests
  var guestsLabel = totalGuests === 1 ? " guest" : " guests";
  // Set the label for rooms depending on whether there is one room or multiple rooms
  var roomsLabel = rooms === "1" ? " room" : " rooms";
  // Set the value of the input field with the guest count and room count labels
  document.getElementById("guests").value =
    totalGuests + guestsLabel + " · " + rooms + roomsLabel;
}
