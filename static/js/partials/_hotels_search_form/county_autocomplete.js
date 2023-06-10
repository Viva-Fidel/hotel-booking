new Autocomplete("#booking-search-form__item-geo", {
  // The search function takes user input and returns a Promise that resolves with an array of results
  search: (input) => {
    const url = "/search/?address=" + input.trim();
    // Using fetch to send an HTTP request to the specified URL and return a Promise that resolves with the response
    return new Promise((resolve) => {
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          resolve(data.data); // Resolving the Promise with the array of results from the response data
        });
    });
  },
});
