let map;
let marker;

function initMap() {
    mapboxgl.accessToken = 'pk.eyJ1IjoibmF3YWJraDIwNDAiLCJhIjoiY2x0aWwydmY2MGRhYzJxbzBnb3ZkZGFwYyJ9.pOki1d8O8P4SW9xX9BrPXA'; // Replace with your Mapbox access token
    map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [75.86471723208145, 22.722357081788935],
        zoom: 9
    });

    map.addControl(new mapboxgl.NavigationControl());

    map.on('load', function() {
        marker = new mapboxgl.Marker({
            draggable: true
        })
            .setLngLat([75.86471723208145, 22.722357081788935])
            .addTo(map);

        marker.on('dragend', function () {
            const lngLat = marker.getLngLat();
            document.getElementById("latitude").value = lngLat.lat;
            document.getElementById("longitude").value = lngLat.lng;
        });
    });
}

function searchLocation() {
    const address = document.getElementById("searchInput").value;

    fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/${address}.json?country=in&access_token=pk.eyJ1IjoibmF3YWJraDIwNDAiLCJhIjoiY2x0aWwydmY2MGRhYzJxbzBnb3ZkZGFwYyJ9.pOki1d8O8P4SW9xX9BrPXA`)
        .then(response => response.json())
        .then(data => {
            const coordinates = data.features[0].center;
            const lat = coordinates[1];
            const lon = coordinates[0];

            // Update latitude and longitude input fields
            document.getElementById("latitude").value = lat;
            document.getElementById("longitude").value = lon;

            // Update map focus
            map.flyTo({
                center: [lon, lat],
                zoom: 12
            });

            // Update marker position
            marker.setLngLat([lon, lat]);
        })
        .catch(error => console.error('Error:', error));
}
document.addEventListener("DOMContentLoaded", function () {
    // Event listeners for opening and closing the map container
    let mapOpenButton = document.getElementById("mapOpenButton");
    let mapOpenButton1 = document.getElementById("mapOpenButton1");
    let mapCloseButton = document.getElementById("mapClose");
    let mapContainer = document.getElementsByClassName("mapContainer");
    let mainBox = document.getElementsByClassName("mainBox");

    mapOpenButton1.addEventListener('click', () => {
        mapContainer.item(0).style.display = "block";
        mainBox.item(0).style.display = "none";
    });

    mapOpenButton.addEventListener('click', () => {
        mapContainer.item(0).style.display = "block";
        mainBox.item(0).style.display = "none";
    });

    mapCloseButton.addEventListener('click', () => {
        mapContainer.item(0).style.display = "none";
        mainBox.item(0).style.display = "block";
    });

    // Initialize the map when the page loads
    initMap();
});
