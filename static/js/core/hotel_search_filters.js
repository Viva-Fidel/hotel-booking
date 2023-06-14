$(document).ready(function () {
    // Define variables to store the selected values
    let selectedPrices = null;
    let hotelRating = null;
    let selectedFacilities = null;
    let selectedActivities = null;
    let hotelType = null;
    let sorting = null; 
    let displayedHotels = 8;
  
    $(".more-results__button").click(function () {
      // Increase the number of displayed hotels by 4
      displayedHotels += 4;
  
      // Call the updateSearchResults function with the updated number of displayed hotels
      updateSearchResults();
    });
  
    // Add event listener to the hotel name input field
    $("#hotel-search-input").keypress(function (event) {
      if (event.which === 13) {
        // Enter key code
        event.preventDefault();
        updateSearchResults();
      }
    });
  
    const allocationButtons = document.querySelectorAll(".allocation-type-filter__button");
  
      allocationButtons.forEach((button) => {
        button.addEventListener("click", () => {
          if (button.classList.contains("selected")) {
            button.classList.remove("selected");
          } else {
            allocationButtons.forEach((otherButton) => {
              otherButton.classList.remove("selected");
            });
            button.classList.add("selected");
          }
          hotelType = getHotelType();
          updateSearchResults();
        });
      });
  
      function getHotelType() {
        const selectedButton = document.querySelector(
          ".allocation-type-filter__button.selected"
        );
        if (selectedButton) {
          return selectedButton.textContent.trim();
        }
        return null;
      }
  
  
  
    $(document).on(
      "change",
      ".filter__item-facility",
      function () {
        selectedFacilities = [];
        $(".filter__item-facility").each(function () {
          if ($(this).is(":checked")) {
            selectedFacilities.push($(this).val());
          }
        });
        updateSearchResults();
      }
    );
  
    $(document).on(
      "change",
      ".filter__item-activity",
      function () {
        selectedActivities = [];
        $(".filter__item-activity").each(function () {
          if ($(this).is(":checked")) {
            selectedActivities.push($(this).val());
          }
        });
        updateSearchResults();
      }
    );
  
    $(document).on(
      "change",
      ".filter__item-price",
      function () {
        selectedPrices = [];
        $(".filter__item-price").each(function () {
          if ($(this).is(":checked")) {
            selectedPrices.push($(this).val());
          }
        });
        updateSearchResults();
      }
    );
  
    const starButtons = document.querySelectorAll(
      ".stars__star-button"
    );
  
    starButtons.forEach((button) => {
      button.addEventListener("click", () => {
        if (button.classList.contains("selected")) {
          button.classList.remove("selected");
        } else {
          starButtons.forEach((otherButton) => {
            otherButton.classList.remove("selected");
          });
          button.classList.add("selected");
        }
        hotelRating = getSelectedRating();
        updateSearchResults();
      });
    });
  
    function getSelectedRating() {
      const selectedButton = document.querySelector(
        ".stars__star-button.selected"
      );
      if (selectedButton) {
        return parseInt(selectedButton.textContent.trim());
      }
      return null;
    }
  
    const dropDownList = document.querySelector(".sort-by__list");
    const dropDownIcon = document.querySelector(".sort-by__icon");
    const sortByContainer = document.querySelector(".sort-by__container");
    const sortByChoice = document.querySelector(".sort-by__default-text");
  
    // Hide the drop-down list on page load
    dropDownList.style.display = "none";
  
    // Toggle the drop-down list when the icon is clicked
    dropDownIcon.addEventListener("click", () => {
      if (dropDownList.style.display === "none") {
        dropDownList.style.display = "flex";
        dropDownIcon.classList.add("rotated");
      } else {
        dropDownList.style.display = "none";
        dropDownIcon.classList.remove("rotated");
      }
    });
  
    // Update the sort-by choice when an item is clicked
    dropDownList.addEventListener("click", (event) => {
      const selectedItem = event.target.closest("li");
      if (selectedItem) {
        sortByChoice.textContent = selectedItem.textContent.trim();
        dropDownList.style.display = "none";
        dropDownIcon.classList.remove("rotated");
        sorting = sortByChoice.textContent; // Set the sorting value based on the selected item
        updateSearchResults();
      }
    });
  
    function updateSearchResults() {
        // Get the search parameters from the URL
        var searchParams = new URLSearchParams(window.location.search);
        var destination = searchParams.get("destination");
        var checkin = searchParams.get("checkin");
        var checkout = searchParams.get("checkout");
        var guests = searchParams.get("guests");
        var hotelName = $("#hotel-search-input").val();
  
        // Create the AJAX request
        $.ajax({
          url: "/update-search-results/",
          type: "GET",
          data: {
            destination: destination,
            checkin: checkin,
            checkout: checkout,
            guests: guests,
            hotel_name: hotelName,
            price: (selectedPrices || []).join(","),
            hotel_rating: hotelRating,
            facilities: (selectedFacilities || []).join(","),
            activities: (selectedActivities || []).join(","),
            hotel_type: hotelType,
            sorting: sorting,
            displayed_hotels: displayedHotels,
          },
          dataType: "json",
          success: function (response) {
            // Parse the JSON response
            var data = response;
            var duration = data.duration;
            var guests = data.guests;
            var numHotelsFound = data.num_hotels_found;
            var priceRanges = data.price_ranges;
            var facilities = data.facilities;
            var activities = data.activities;
            var hotelResults = data.hotel_results;
  
            console.log(facilities)
  
            var checkedStatePrice = {};
            $("input[name='price-range']").each(function () {
              checkedStatePrice[$(this).val()] = $(this).is(":checked");
            });
            var checkedStateFacility = {};
            $("input[name='facility-range']").each(function () {
              checkedStateFacility[$(this).val()] = $(this).is(":checked");
            });
  
            var checkedStateActivity = {};
            $("input[name='activity-range']").each(function () {
              checkedStateActivity[$(this).val()] = $(this).is(":checked");
            });
            
            $; // Update the price range list
            $("#price-list").empty();
            priceRanges.forEach(function (price) {
              var checked = checkedStatePrice[price.value] ? "checked" : "";
              var listItem = `
      <li class="filter__item">
        <input
          type="checkbox"
          name="price-range"
          value="${price.value}"
          class="filter__item-price"
          ${checked}
        />
        ${price.label}
        <span>${price.count}</span>
      </li>
    `;
              $("#price-list").append(listItem);
            });
  
            $("#facilities-list").empty();
            facilities.forEach(function (facility) {
              var checked = checkedStateFacility[facility.value] ? "checked" : "";
              var listItem = `
      <li class="filter__item">
        <input
          type="checkbox"
          name="facility-range"
          value="${facility.value}"
          class="filter__item-facility"
          ${checked}
        />
        ${facility.label}
        <span>${facility.count}</span>
      </li>
    `;
              $("#facilities-list").append(listItem);
              console.log(listItem);
            });
  
            $("#activities-list").empty();
  
            activities.forEach(function (activity) {
              var checked = checkedStateActivity[activity.value] ? "checked" : "";
              var listItem = `
                <li class="filter__item">
                  <input
                    type="checkbox"
                    name="activity-range"
                    value="${activity.value}"
                    class="filter__item-activity"
          ${checked}
                  />
                  ${activity.label}
                  <span>${activity.count}</span>
                </li>
              `;
  
              // Append the list item to the price range list
              $("#activities-list").append(listItem);
            });
  
            // Clear the existing search results
            $("#search-results-list").empty();
  
            if (hotelResults.length > 0) {
              // Loop through the hotel results and append the updated HTML
              hotelResults.forEach(function (hotelResult) {
                var html = "";
  
                // Generate the HTML for each hotel result
                html += `
                  <li class="search-results__item">
                    <img
                      src="${hotelResult.hotel_cover_photo}"
                      alt="${hotelResult.hotel_name}"
                      class="search-results__item-image"
                    />
                    <div class="hotel-info__container">
                      <div class="hotel-info__title-container">
                        <h4 class="hotel-info__title">
                          <a href="${hotelResult.hotel_link}" class="hotel-info__link" target="_blank">${hotelResult.hotel_name}</a>
                        </h4>
                        ${
                          hotelResult.special_discount != 0
                            ? `
                              <div class="hotel-info__promo_active">
                                ${hotelResult.special_discount}
                              </div>
                            `
                            : `
                              <div class="hotel-info__promo_not-active"></div>
                            `
                        }
                      </div>
  
                      <div class="hotel-info__rating-container">
                        <div class="hotel-info__rating-stars-container">
                          
                        </div>
                        <p class="hotel-info__rating-stars-text">
                          Guest rating: ${hotelResult.user_rating} (${hotelResult.amount_of_reviews} Reviews)
                        </p>
                      </div>
  
                      <div class="hotel-info__description-container">
                        <div class="hotel-info__description-container-left">
                          <p class="hotel-info__description-container-left-title">
                            ${hotelResult.hotel_search_info_title}
                          </p>
                          <p class="hotel-info__description-container-left-text">
                            ${hotelResult.hotel_search_info_text}
                          </p>
                          <button type="submit" class="hotel-info__description-container-left-button">
                            <a href=${hotelResult.hotel_link} class="hotel-info__description-container-left-link" target="_blank">See availability</a>
                          </button>
                        </div>
                        <div class="hotel-info__description-container-right">
                          ${
                            hotelResult.total_price_with_discount != 0
                              ? `
                                <div class="hotel-info__description-container-right-discount hotel-info__description-container-right-discount_active">
                                  ${hotelResult.price_discount}% off
                                </div>
                              `
                              : `
                                <div class="hotel-info__description-container-right-discount hotel-info__description-container-right-discount_not-active"></div>
                              `
                          }
                          <p class="hotel-info__description-container-right-duration-text">
                            ${guests} ${duration} days
                          </p>
                          ${
                            hotelResult.total_price_with_discount != 0
                              ? `
                                <p class="hotel-info__description-container-right-price-full">
                                  US$${hotelResult.total_price_with_discount}
                                </p>
                                <p class="hotel-info__description-container-right-price-discount hotel-info__description-container-right-price-discount_active">
                                  US$${hotelResult.total_price}
                                </p>
                              `
                              : `
                                <p class="hotel-info__description-container-right-price-full">
                                  US$${hotelResult.total_price}
                                </p>
                                <div class="hotel-info__description-container-right-price-discount hotel-info__description-container-right-price-discount_not-active"></div>
                              `
                          }
                          <p class="hotel-info__description-container-right-price-taxes">
                            Includes taxes and fees
                          </p>
                        </div>
                      </div>
                    </div>
                  </li>
                `;
  
                // Append star icons based on hotel rating
                var $hotelResultItem = $(html);
                $("#search-results-list").append($hotelResultItem);
  
                // Append star icons based on hotel rating
                var $ratingStarsContainer = $hotelResultItem.find(
                  ".hotel-info__rating-stars-container"
                );
                for (var i = 0; i < hotelResult.hotel_rating; i++) {
                  $ratingStarsContainer.append(
                    $("<img>")
                    .attr("src", staticUrl + "images/core/icons/star.png")
                      .attr("alt", "Star icon")
                      .addClass(
                        "hotel-info__rating-stars-star-icon"
                      )
                  );
                }
              });
  
              $("#num-hotels-found").text(numHotelsFound);
            } else {
              // No hotel results found, display a message
              var message = `
                <li class="search-results__no-results">
                  <p>No hotels found for the specified search parameters.</p>
                </li>
              `;
  
              // Append the message to the search results container
              $("#search-results-list").append(message);
              $("#num-hotels-found").text(numHotelsFound);
            }
          },
        });
      }
    });