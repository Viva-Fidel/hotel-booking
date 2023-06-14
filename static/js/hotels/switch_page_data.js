function showOverview(button) {
    setActiveButton(button);
    document.getElementById("hotel-data-container").style.display = "flex";
    document.getElementById("room-data-container").style.display = "none";
    document.getElementById("reviews-data-container").style.display = "none";
  }

  function showRooms(button) {
    setActiveButton(button);
    document.getElementById("hotel-data-container").style.display = "none";
    document.getElementById("room-data-container").style.display = "flex";
    document.getElementById("reviews-data-container").style.display = "none";
  }

  function showGuestReviews(button) {
    setActiveButton(button);
    document.getElementById("hotel-data-container").style.display = "none";
    document.getElementById("room-data-container").style.display = "none";
    document.getElementById("reviews-data-container").style.display = "flex";
  }

  function setActiveButton(button) {
    var buttons = document.getElementsByClassName("page-menu__button");
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].classList.remove("active");
    }
    button.classList.add("active");
  }