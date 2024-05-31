// Inicializar el mapa
var map = L.map('map').setView([0, 0], 2); // Coordenadas iniciales y nivel de zoom
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Crear un grupo de marcadores con clustering
var markers = L.markerClusterGroup();

// Función para actualizar los marcadores del mapa
function updateMap() {
    fetch('/api/data/charts/map')
        .then(response => response.json())
        .then(data => {
            data.data.forEach(function (doc) {
                var marker = L.circleMarker(doc.coords, {
                    radius: 10,
                    fillColor: "#0078FF",
                    color: "#000",
                    weight: 1,
                    opacity: 1,
                    fillOpacity: 0.8
                }).bindTooltip(doc.count + ' documentos', {permanent: true, direction: 'top'}).openTooltip();
                markers.addLayer(marker);
            });
            map.addLayer(markers);
        })
        .catch(error => console.error('Error fetching map data:', error));
}
