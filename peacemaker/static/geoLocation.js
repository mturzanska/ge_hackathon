document.onreadystatechange = function() {
	var state = document.readyState
	if (state == 'interactive') {
	} else if (state == "complete") {
	    setTimeout(function() {
                document.getElementById('interactive');
		document.getElementById('loader').style.visibility="hidden";
	    }, 1);
	}
}

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
