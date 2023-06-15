// Selecting the HTML elements for the check-in and check-out date inputs
const checkIn = document.getElementById("checkin");
const checkOut = document.getElementById("checkout");
const submitButton = document.querySelector(".room-search-form__submit-button");

// Setting the maximum date for the check-out input to one year from today
const maxDate = new Date();
maxDate.setFullYear(maxDate.getFullYear() + 1);

// Initializing Flatpickr for the check-out input with options for date formatting, minimum and maximum dates, and event handling
const checkOutPicker = flatpickr(checkOut, {
  altInput: checkOut, // Using an alternate input field for better accessibility
  minDate: "today", // Setting the minimum date to today
  maxDate: maxDate, // Setting the maximum date to one year from today
  dateFormat: "d-m-Y", // Specifying the date format as day-month-year
  onClose: function (selectedDates, dateStr, instance) {
    // Handling the event when the user selects a check-out date
    if (checkIn.value != "" && selectedDates[0] >= new Date(checkIn.value)) {
      // If a check-in date has already been selected and the selected check-out date is later than the check-in date,
      // clear the check-out input and set the minimum date for the check-in input to the selected check-out date
      instance.clear();
      checkIn._flatpickr.set("minDate", dateStr);
    } else {
      // If no check-in date has been selected or the selected check-out date is earlier than the check-in date,
      // set the minimum date for the check-in input to today and the maximum date for the check-out input to the maximum date allowed
      checkIn._flatpickr.set("minDate", "today");
      checkIn._flatpickr.set("maxDate", dateStr);
    }
  },
});

// Initializing Flatpickr for the check-in input with options for date formatting, minimum date, and event handling
const checkInPicker = flatpickr(checkIn, {
  altInput: checkIn, // Using an alternate input field for better accessibility
  minDate: "today", // Setting the minimum date to today
  dateFormat: "d-m-Y", // Specifying the date format as day-month-year
  onClose: function (selectedDates, dateStr, instance) {
    // Handling the event when the user selects a check-in date
    if (
      checkOut.value != "" &&
      selectedDates[0] >= new Date(checkOut.value)
    ) {
      // If a check-out date has already been selected and the selected check-in date is later than the check-out date,
      // clear the check-in input and set the minimum date for the check-out input to the selected check-in date
      instance.clear();
      checkOut._flatpickr.set("minDate", dateStr);
    } else {
      // If no check-out date has been selected or the selected check-in date is earlier than the check-out date,
      // set the minimum date for the check-out input to the selected check-in date and the maximum date for the check-out input to the maximum date allowed
      checkOut._flatpickr.set("minDate", dateStr);
      checkOut._flatpickr.set("maxDate", maxDate);
    }
  },
});

// Event listener for the search button click
submitButton.addEventListener("click", function(event) {
  // Check if check-in and check-out dates are not selected
  if (checkIn.value === "" && checkOut.value === "") {
    // Set default dates as 7 days from today
    const defaultCheckInDate = new Date();
    const defaultCheckOutDate = new Date();
    defaultCheckInDate.setDate(defaultCheckInDate.getDate() + 7);
    defaultCheckOutDate.setDate(defaultCheckInDate.getDate() + 7);
    
    // Format the default dates as "d-m-Y"
    const defaultCheckInDateStr = `${defaultCheckInDate.getDate()}-${defaultCheckInDate.getMonth() + 1}-${defaultCheckInDate.getFullYear()}`;
    const defaultCheckOutDateStr = `${defaultCheckOutDate.getDate()}-${defaultCheckOutDate.getMonth() + 1}-${defaultCheckOutDate.getFullYear()}`;
    
    // Set the default dates in the input fields and update the Flatpickr instances
    checkIn.value = defaultCheckInDateStr;
    checkOut.value = defaultCheckOutDateStr;
    checkInPicker.setDate(defaultCheckInDate);
    checkOutPicker.setDate(defaultCheckOutDate);
  }
  else if (checkIn.value === "" && checkOut.value !== "") {
  // If only check-out date is selected, set default check-in date as 1 day before the selected check-out date
  const selectedCheckOutDateParts = checkOut.value.split("-");
  const selectedCheckOutDate = new Date(
    parseInt(selectedCheckOutDateParts[2]),
    parseInt(selectedCheckOutDateParts[1]) - 1,
    parseInt(selectedCheckOutDateParts[0])
  );
  const defaultCheckInDate = new Date(selectedCheckOutDate);
  defaultCheckInDate.setDate(selectedCheckOutDate.getDate() - 1);

  // Format the default check-in date as "d-m-Y"
  const defaultCheckInDateStr = `${defaultCheckInDate.getDate()}-${defaultCheckInDate.getMonth() + 1}-${defaultCheckInDate.getFullYear()}`;

  // Set the default check-in date in the input field and update the Flatpickr instance
  checkIn.value = defaultCheckInDateStr;
  checkInPicker.setDate(defaultCheckInDate);
  checkOutPicker.setDate(selectedCheckOutDate); // Update the check-out date in the Flatpickr instance
} else if (checkIn.value !== "" && checkOut.value === "") {
  // If only check-in date is selected, set default check-out date as 1 day after the selected check-in date
  const selectedCheckInDateParts = checkIn.value.split("-");
  const selectedCheckInDate = new Date(
    parseInt(selectedCheckInDateParts[2]),
    parseInt(selectedCheckInDateParts[1]) - 1,
    parseInt(selectedCheckInDateParts[0])
  );
  const defaultCheckOutDate = new Date(selectedCheckInDate);
  defaultCheckOutDate.setDate(selectedCheckInDate.getDate() + 1);

  // Format the default check-out date as "d-m-Y"
  const defaultCheckOutDateStr = `${defaultCheckOutDate.getDate()}-${defaultCheckOutDate.getMonth() + 1}-${defaultCheckOutDate.getFullYear()}`;

  // Set the default check-out date in the input field and update the Flatpickr instance
  checkOut.value = defaultCheckOutDateStr;
  checkOutPicker.setDate(defaultCheckOutDate);
  checkInPicker.setDate(selectedCheckInDate); // Update the check-in date in the Flatpickr instance
}
});