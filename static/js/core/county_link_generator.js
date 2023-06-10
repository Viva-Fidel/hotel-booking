// Get the link element
var link = document.getElementById('county-link');

// Attach a click event listener to the link
link.addEventListener('click', function(event) {
  event.preventDefault(); // Prevent the default link behavior

  // Extract the necessary parameters from the link's attributes
  var destination = encodeURIComponent(link.getAttribute('href').split('?destination=')[1].split('&')[0]);
  var checkin = encodeURIComponent(link.getAttribute('href').split('&checkin=')[1].split('&')[0]);
  var checkout = encodeURIComponent(link.getAttribute('href').split('&checkout=')[1].split('&')[0]);
  var guests = encodeURIComponent(link.getAttribute('href').split('&guests=')[1].split('&')[0]);

  // Construct the URL with the parameters
  var url = '/search/hotels/?destination=' + destination + '&checkin=' + checkin + '&checkout=' + checkout + '&guests=' + guests;

  // Perform the GET request or redirect to the generated URL
  window.location.href = url;
});