function loadMapScenario() {
    var map = new Microsoft.Maps.Map(document.getElementById("myMap"), {
      /* No need to set credentials if already passed in URL */
      center: new Microsoft.Maps.Location(
        45.52643797510934,
        -122.60225638970428
      ),
      zoom: 15,
    });

    Microsoft.Maps.loadModule("Microsoft.Maps.Search", function () {
      var searchManager = new Microsoft.Maps.Search.SearchManager(map);
      var requestOptions = {
        bounds: map.getBounds(),
        where: address,
        callback: function (answer, userData) {
          map.setView({ bounds: answer.results[0].bestView });
          map.entities.push(
            new Microsoft.Maps.Pushpin(answer.results[0].location)
          );
          var entityLookupRequestOptions = {
            location: new Microsoft.Maps.Location(
              answer.results[0].location.latitude,
              answer.results[0].location.longitude
            ),
            callback: function (answer) {
              if (answer) {
                console.log(answer);
                var exploreContainer = document.querySelector(
                  ".hotel-data__explore-container"
                );

                for (
                  var i = 0, len = answer.businessesAtLocation.length;
                  i < len;
                  i++
                ) {
                  var business = answer.businessesAtLocation[i].entityName;
                  var exploreItemContainer = document.createElement("div");
                  exploreItemContainer.className =
                    "hotel-data__explore-item";

                  var iconImg = document.createElement("img");
                  iconImg.src = staticUrl;
                  iconImg.alt = "Geolocation icon";
                  iconImg.className =
                    "hotel-data__explore-item-icon";

                  var textP = document.createElement("p");
                  textP.className =
                    "hotel-data__explore-item-text";
                  textP.textContent = business;

                  exploreItemContainer.appendChild(iconImg);
                  exploreItemContainer.appendChild(textP);
                  exploreContainer.appendChild(exploreItemContainer);
                }
              }
            },
          };
          searchManager.entityLookup(entityLookupRequestOptions);
        },
      };

      searchManager.geocode(requestOptions);
    });
  }