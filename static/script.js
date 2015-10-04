
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

        var parsed_data = JSON.parse(data);

        for (var k = 0; k < parsed_data.length; k++) {
            locations.push(parsed_data[k])
        }

        var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        var labelIndex = 0;
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
            marker = new google.maps.Marker({
                position: new google.maps.LatLng(locations[i][0], locations[i][1]),
                map: map,
                label: labels[labelIndex++ % labels.length],
            });

            google.maps.event.addListener(marker, 'click', (function (marker, i) {
                return function () {
                    // can edit locations[i][0] to be the text in label
                    var content = '<div style="color:black;"><span style="color:red; text-align:center; font-size: 2em">'
                        + locations[i][0] + ', ' + locations[i][1] + '</span><br />' + '<b>Most common event: ' +
                        '</b>' + locations[i][3] + '<br />' + '<b>Number of people: </b>' + locations[i][4] + '</div>';
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
    });
}