function getLocation() {
    $('.locationBtn').text('');
    $('.locationBtn').prop('class', 'loader');
    $('#loader_text').css('opacity', '1');
    $('#loader_text').css('visibility', 'visible');


    if (navigator.geolocation) {
        geoLocation = navigator.geolocation.getCurrentPosition(getLatLon, geoLocationError, {timeout: 8000});
    } else {
        alert('Geolocation is not supported by your browser');
    }
}

function geoLocationError(error) {
  console.error(error);
}

function loaderTextUpdater(message, timeout) {
    setTimeout(function() {
      $('#loader_text').css('opacity', '0');
      setTimeout(function() {
        $('#loader_text p').text(message);
        $('#loader_text').css('opacity', '1');
      }, 100);
    }, timeout);
}

function getLatLon(position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    var data = {
        'latitude': latitude,
        'longitude': longitude
    };

    loaderTextUpdater('Almost there', 5000);
    loaderTextUpdater('Working', 9000);

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

$(document).ready(function() {
  $('.locationBtn').click(getLocation);
});
