
function initialize() {
    var glasgow = new google.maps.LatLng(55, -4);
    var mapCanvas = document.getElementById('map');
    var mapOptions = {
        center: glasgow,
        zoom: 10,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(mapCanvas, mapOptions);
}
google.maps.event.addDomListener(window, 'load', initialize);

function analyse() {
    $.get('/sas/get_locations', function(data) {
        var locations = [];
        var officers_to_deploy_json = $('#officers-number').attr('value');

        var officers_to_deploy = JSON.parse(officers_to_deploy_json);
        var parsed_data = JSON.parse(data);

        for (var k = 0; k < parsed_data.length; k++) {
            locations.push(parsed_data[k])
        }

        var glasgow = new google.maps.LatLng(55, -4);
        //var locations = {{ coords }}
        var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 10,
            center: glasgow,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        var infowindow = new google.maps.InfoWindow();


        var marker, i;
        for (i = 0; i < locations.length; i++) {
          var pinImage = new google.maps.MarkerImage("https://chart.googleapis.com/chart?chst=d_map_spin&" + "chld=1|0|ff1919|20|b|"+(i+1));
            if (i < 5) {
                marker = new google.maps.Marker({
                    position: new google.maps.LatLng(locations[i][0], locations[i][1]),
                    map: map,
                    icon: pinImage
                });
            }
            else {
                var pinColor = "2d70c6";
                var pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor,
                new google.maps.Size(21, 34),
                new google.maps.Point(0,0),
                new google.maps.Point(10, 34));
                marker = new google.maps.Marker({
                    position: new google.maps.LatLng(locations[i][0], locations[i][1]),
                    map: map,
                    icon: pinImage
                });
            }

            google.maps.event.addListener(marker, 'click', (function (marker, i) {
                return function () {
                    // can edit locations[i][0] to be the text in label
                    var content = '<div style="color:black;"><span style="color:#2d70c6; text-align:center; font-size: 2em">'
                        + locations[i][0] + ', ' + locations[i][1] + '</span><br />' + '<b>Most common event: ' +
                        '</b>' + locations[i][3] + '<br />' + '<b>Number of people: </b>' + locations[i][4] +
                        '<br /><b>' + officers_to_deploy[i] + '</b> officers should be deployed in this area</div>';
                    infowindow.setContent(content);
                    infowindow.open(map, marker);
                }
            })(marker, i));
        }
    });
}
function back() {
    window.location.href='/sas/'
}
function deploy() {
    var groups = $('#groups').val();
    var officers = $('#officers').val();
    window.location.href='/sas/deploy?groups=' + groups + '&officers=' + officers;
}
function analyseAreas() {
    $.get('/sas/get_locations', function(data) {
        var locations = [];

        var parsed_data = JSON.parse(data);

        for (var k = 0; k < parsed_data.length; k++) {
            locations.push(parsed_data[k])
        }

        var glasgow = new google.maps.LatLng(55, -4);
        var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 10,
            center: glasgow,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        });
        for (i = 0; i < locations.length; i++) {
            var circle = new google.maps.Circle({
                strokeColor: '#1b4376',
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: '#1b4376',
                fillOpacity: 0.35,
                map: map,
                center: {lat: locations[i][0], lng: locations[i][1]},
                radius: Math.sqrt(locations[i][2]) * 100
            });
        }
    });
}
