var cities = [{
  city: 'Colorado Springs',
  desc: 'UCCS!',
  lat: 38.893079,
  long: -104.800931
}];
/*
---------- Components of an AngularJS Application ----------

AngularJS provides a front end framework based on the MVC model. It is built on top of JavaScript and JQuery. With MVC the Model represents the data source, the View is the rendered page, and the Controller handles communication between both of them. By structuring your page this way your code is easier to maintain, easier to update and makes for more readable code.

AngularJS uses modules which represent the components used in your application. Using modules makes it easy to reuse your code in many applications.

Web pages are normally manipulated by working with the DOM object in JavaScript and JQuery. AngularJS allows you to extend HTML tags and attributes using AngularJS directives which make it easy to bind data directly to HTML elements.

AngularJS uses JavaScript objects to represent data called Scope which can be data generated on the web server, a database, web service, or client side AngularJS code.

You can use expressions that are directly linked to the scope (data) so that the page is updated dynamically as the data changes. Data binding works as well so that when data changes on the web page the model is also updated.

Many services are provided for common tasks like using AJAX techniques to dynamically pull data from a web service or the server.
*/

// Here we implement the template, module, controller and scope

// Define the AngularJS Module
// Modules are used to
// 1. Associate an AngularJS app with part of an HTML document
// 2. Provide access to AngularJS features
// 3. Help with organization
// angular.module() excepts the module name, list of modules this module
// needs and an optional configuration for the module. Modules that work with
// HTML normally have a name that contains app.

var medApp = angular.module('medLookUp', [])

//changes how data is spliced into html istead of the default {{}}
//we now use {[{}]}
//because Django's default is already {{}}
medApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{')
  $interpolateProvider.endSymbol('}]}')
})

// Define the Controller and implement the Scope which links HTML
// elements to variables in the Scope. It receives the controller
// name and a factory function which gets the controller ready to use
// We are saying that $scope is a dependency and that we want Angular
// to pass in the $scope object when the function is called. This is
// an example of dependency injection. Angular sees that my factory
// function contains the $scope component and then it gets it and passes
// it to the function automatically.


//controller for interaction pages
medApp.controller('interactionsCtrl', function($scope, $http, $window) {

  //waits for angular to load before displaying to html
  $scope.style = {
    display: 'block'
  }

  //controller variables in scope
  $scope.banner = ""
  $scope.medication = ""
  $scope.interactionMeds = ""
  $scope.status = ""
  $scope.lowestPrice = ""


  //interactions page submit button function
  $scope.submitInteractions = function() {
    if ($scope.interactionMeds) {
      $scope.banner = "Searching for interactions in: " + $scope.interactionMeds + "..."
    }
    //calls function to make api call to backend
    interactionsApiCall($scope.interactionMeds)
  }

  //interactions page URL param function
  $scope.submitInteractionsFromURL = function(medication) {
    $scope.interactionMeds = medication
    if ($scope.interactionMeds) {
      $scope.banner = "Searching for interactions in: " + $scope.interactionMeds + "..."
    }
    //calls function to make api call to backend
    interactionsApiCall($scope.interactionMeds)
  }

  //interactions page api call function
  function interactionsApiCall(medication) {
    $scope.interaction = ""
    $http.get('/interactionsAPI/' + medication).then(function(response) {
      $scope.interaction = response.data
      $scope.status = response.status
    }, function(response) {
      $scope.data = response.data || 'Request failed'
      $scope.status = response.status
      if ($scope.status >= 400) {
        $scope.banner = "Unable to find: " + $scope.medication
        $scope.interaction = ""
      }
    })

  }

  $scope.range = function(min, max, step) {
    step = step || 1;
    var input = [];
    for (var i = min; i <= max; i += step) input.push(i);
    return input;
  }
})

//Angular controller for the home page (price and maps)
medApp.controller('homeCtrl', function($scope, $http, $window) {

  //waits for angular to load before displaying to html
  $scope.style = {
    display: 'block'
  }

  //controller variables in scope
  $scope.banner = ""
  $scope.exactPrice = ""
  $scope.exactPriceLink = ""
  $scope.location = ""
  $scope.medication = ""
  $scope.interactionMeds = ""
  $scope.status = ""
  $scope.lowestPrice = ""
  $scope.lowestPriceTitle = ""
  $scope.lowestPriceQuantity = ""

  //home page submit button function
  $scope.submit = function() {

    //checks user input (user does NOT have to enter a location for this to work)
    if ($scope.location && $scope.medication) {

      //sets up GoodRx link with inputted medication
      $scope.exactPrice = "Click here to find exact pricing at local pharmacies for: " + $scope.medication + " at GoodRx.com"
      $scope.exactPriceLink = "https://www.goodrx.com/" + $scope.medication

      //Shows when search has begun
      $scope.banner = "Searching for: " + $scope.medication + " in: " + $scope.location + "..."

      //calls function to make api call to backend
      createMap($scope.location)
      //calls function to make api call to backend
      apiCall($scope.medication)

    } else if ($scope.medication && $scope.location == "") {

      //sets up GoodRx link with inputted medication
      $scope.exactPrice = "Click here to find exact pricing at local pharmacies for: " + $scope.medication + " at GoodRx.com"
      $scope.exactPriceLink = "https://www.goodrx.com/" + $scope.medication

      //Shows when search has begun
      $scope.banner = "Searching for: " + $scope.medication + "..."

      //calls function to make api call to backend
      apiCall($scope.medication)
    }
  }

  //home page api call function
  function apiCall(medication) {

    //calls the backend to retrieve data on pricing (JSON)
    $http.get('/local/' + medication).then(function(response) {

      //saves data to scope variable
      $scope.local = response.data

      //sets the lowest price (price, name quantity) for displaying on maps
      $scope.lowestPrice = response.data[0].totalPrice[0]
      $scope.lowestPriceTitle = response.data[0].title
      $scope.lowestPriceQuantity = response.data[0].quantity[0]

      //saves response
      $scope.status = response.status

      //ran if no response to the backend was successful
    }, function(response) {
      $scope.data = response.data || 'Request failed'
      $scope.status = response.status
      if ($scope.status >= 400) {
        $scope.banner = "Unable to find: " + $scope.medication
        $scope.local = ""
      }
    })
  }

  //used for looping inside of html
  $scope.range = function(min, max, step) {
    step = step || 1;
    var input = [];
    for (var i = min; i <= max; i += step) input.push(i);
    return input;
  }

  //////////////////////////////////////////////////////////////////////////////
  ////////BEGIN MAPS API--------------------------------------------------------
  //////////////////////////////////////////////////////////////////////////////

  $scope.lat = "38.893137"
  $scope.lng = "-104.800630"


  function createMap(location) {

    //calls backend api to convert location to lat&lng then return pharmacies at said lat&lng
    $http.get('/mapsAPI/' + location).then(function(response) {

      $scope.mapData = response.data.results || 'Request failed'
      $scope.mapStatus = response.status

      //centers map on first pharmacy
      var mapOptions = {
        zoom: 11,
        center: new google.maps.LatLng($scope.mapData[0].geometry.location.lat, $scope.mapData[0].geometry.location.lng),
        mapTypeId: google.maps.MapTypeId.TERRAIN
      }

      //where to display map in html
      if (document.getElementById('map')) {
        $scope.map = new google.maps.Map(document.getElementById('map'), mapOptions);
      }

      //info window is opened on pin click
      var infoWindow = new google.maps.InfoWindow();

      //creates marker on map
      $scope.markers = [];
      var createMarker = function(info) {
        var marker = new google.maps.Marker({
          map: $scope.map,
          position: new google.maps.LatLng(info.geometry.location.lat, info.geometry.location.lng),
          title: info.name
        });

        //info window is opened on pin click
        google.maps.event.addListener(marker, 'click', function() {
          infoWindow.setContent('<h2 class="mb-0">' + marker.title + '</h2>' +
            '<h4 class="mb-0">Estimated: ' + $scope.lowestPrice + '<span style="font-size: 12px;">(May not be actual price)</span></h4>' +
            '<p class="mb-0">' + $scope.lowestPriceTitle + 'Quantity: ' + $scope.lowestPriceQuantity + '</p>' +
            '<a href="https://www.google.com/maps/place/' + info.formatted_address + '">' + info.formatted_address + '</a>');

          infoWindow.open($scope.map, marker);
        });

        //pushes marker to map
        $scope.markers.push(marker);
      }



      //calls above function for every input recieved from backend call
      for (i = 0; i < $scope.mapData.length; i++) {
        createMarker($scope.mapData[i]);
      }


      $scope.openInfoWindow = function(e, selectedMarker) {
        e.preventDefault();
        google.maps.event.trigger(selectedMarker, 'click');
      }

      //if response failed
      if ($scope.status >= 400) {
        $scope.banner = "Unable to find pharmacies at: " + $scope.medication
        $scope.interaction = ""
      }
    })
  }

  //////////////////////////////////////////////////////////////////////////////
  ////////Below is the default map that appears on load-------------------------
  //////////////////////////////////////////////////////////////////////////////
  var mapOptions = {
    zoom: 11,
    center: new google.maps.LatLng($scope.lat, $scope.lng),
    mapTypeId: google.maps.MapTypeId.TERRAIN
  }
  if (document.getElementById('map')) {
    $scope.map = new google.maps.Map(document.getElementById('map'), mapOptions);
  }
  var uccs = new google.maps.LatLng($scope.lat, $scope.lng);
  var infoWindow = new google.maps.InfoWindow();
  $scope.markers = [];
  var createMarker = function(info) {
    var marker = new google.maps.Marker({
      map: $scope.map,
      position: new google.maps.LatLng(info.lat, info.long),
      title: info.city
    });
    marker.content = '<div class="infoWindowContent">' + info.desc + '</div>';
    google.maps.event.addListener(marker, 'click', function() {
      infoWindow.setContent('<h2>' + marker.title + '</h2>' + marker.content);
      infoWindow.open($scope.map, marker);
    });
    $scope.markers.push(marker);
  }
  for (i = 0; i < cities.length; i++) {
    createMarker(cities[i]);
  }
  $scope.openInfoWindow = function(e, selectedMarker) {
    e.preventDefault();
    google.maps.event.trigger(selectedMarker, 'click');
  }
  //////////////////////////////////////////////////////////////////////////////
  ////////end default map-------------------------------------------------------
  //////////////////////////////////////////////////////////////////////////////

})
