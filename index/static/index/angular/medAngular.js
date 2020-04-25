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


//because Django :[
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

medApp.controller('homeCtrl', function($scope, $http, $window) {

  $scope.style = {
    display: 'block'
  }

  $scope.banner = ""
  $scope.location = ""
  $scope.medication = ""
  $scope.interactionMeds = ""
  $scope.status = ""

  //home page submit button function
  $scope.submit = function() {
    if ($scope.location && $scope.medication) {
      $scope.banner = "Searching for: " + $scope.medication + " at: " + $scope.location + "..."
      apiCall($scope.medication)
      //do something with location
    } else if ($scope.medication && $scope.location == "") {
      $scope.banner = "Searching for: " + $scope.medication + "..."
      apiCall($scope.medication)
    }
  }

  //home page api call function
  function apiCall(medication) {
    $http.get('/local/' + medication).then(function(response) {
      $scope.local = response.data
      $scope.status = response.status
    }, function(response) {
      $scope.data = response.data || 'Request failed'
      $scope.status = response.status
      if ($scope.status >= 400) {
        $scope.banner = "Unable to find: " + $scope.medication
        $scope.local = ""
      }
    })

  }

  //interactions page submit button function
  $scope.submitInteractions = function() {
    if ($scope.interactionMeds) {
      $scope.banner = "Searching for interactions in: " + $scope.interactionMeds + "..."
    }
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

medApp.controller('mapsCtrl', function($scope) {


  $scope.lat = "38.893137"
  $scope.lng = "-104.800630"

  if (google == null) {
    console.log("var google is undefined")
  } else {

    var mapOptions = {
      zoom: 11,
      center: new google.maps.LatLng($scope.lat, $scope.lng),
      mapTypeId: google.maps.MapTypeId.TERRAIN
    }

    if (document.getElementById('map')) {
      $scope.map = new google.maps.Map(document.getElementById('map'), mapOptions);
    }

    $scope.markers = [];

    var infoWindow = new google.maps.InfoWindow();

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
  }

})
