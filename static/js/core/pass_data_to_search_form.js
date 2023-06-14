window.addEventListener('DOMContentLoaded', (event) => {
    const params = new URLSearchParams(window.location.search); // Get the query parameters from the URL
    const destination = params.get('destination'); // Get the value of the 'destination' parameter
    const checkin = params.get('checkin'); // Get the value of the 'checkin' parameter
    const checkout = params.get('checkout'); // Get the value of the 'checkout' parameter
    const guests = params.get('guests'); // Get the value of the 'guests' parameter

    // Set the values of the input fields using the retrieved query parameters
    document.getElementById('destination').value = destination;
    document.getElementById('checkin').value = checkin;
    document.getElementById('checkout').value = checkout;
    document.getElementById('guests').value = guests;
  });