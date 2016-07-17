function getLocation() {
    if (navigator.geolocation) {
        geoLocation = navigator.geolocation.getCurrentPosition(getLatLon); 
    } else {
        alert('Geolocation is not supported by your browser');
    }	         
}

function getLatLon(position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    var data = {
        'latitude': latitude,
        'longitude': longitude
    };

    $.ajax({
        type: 'POST',
        url: '/',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        success: function(response) {
	    window.location.replace(response.redirect)
	}
    });
}
