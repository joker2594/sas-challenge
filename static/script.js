function initialize() {
  var glasgow = new google.maps.LatLng(55.864131, -4.251427);
  var mapCanvas = document.getElementById('map');
  var mapOptions = {
    center: glasgow,
    zoom: 16,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  }
  var map = new google.maps.Map(mapCanvas, mapOptions);
}
google.maps.event.addDomListener(window, 'load', initialize);

var locations = [
   [55.864131, -4.251427, 1],
   [55.861173, -4.250196, 2],
   [55.861802, -4.243851, 3],
   [55.861290, -4.257208, 4]
];

function analyse() {
  var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  var labelIndex = 0;
  var glasgow = new google.maps.LatLng(55.864131, -4.251427);
  //var locations = {{ coords }}
   var map = new google.maps.Map(document.getElementById('map'), {
     zoom: 16,
     center: glasgow,
     mapTypeId: google.maps.MapTypeId.ROADMAP
   });

   var infowindow = new google.maps.InfoWindow;
   var marker, i;

   for (i = 0; i < locations.length; i++) {
     marker = new google.maps.Marker({
          position: new google.maps.LatLng(locations[i][0], locations[i][1]),
          map: map,
          label: labels[labelIndex++ % labels.length],
        });
        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
              // can edit locations[i][0] to be the text in label
            infowindow.setContent(locations[i][0]);
            infowindow.open(map, marker);
        }
      })(marker, i));
    }
}

function back() {
  window.location.href='/sas/'
}

function deploy() {
  window.location.href='/sas/deploy'
}

function analyseAreas() {
    var glasgow = new google.maps.LatLng(55.864131, -4.251427);
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 16,
      center: glasgow,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    for (i = 0; i < locations.length; i++) {
      var circle = new google.maps.Circle({
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        map: map,
        center: {lat: locations[i][0], lng: locations[i][1]},
        radius: Math.sqrt(locations[i][2]) * 100
      });
    }
  }
