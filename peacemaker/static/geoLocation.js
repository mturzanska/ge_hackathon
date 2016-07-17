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
    console.log(latitude)
    console.log(longitude)
}
