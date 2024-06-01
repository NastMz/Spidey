// Inicializar el mapa
var map = L.map('map').setView([0, 0], 2); // Coordenadas iniciales y nivel de zoom
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Crear un grupo de marcadores con clustering
var markers = L.markerClusterGroup({
    iconCreateFunction: createClusterIcon
});

// Definir la función para crear el ícono del cluster
function createClusterIcon(cluster) {
    // Obtener todos los marcadores dentro del cluster
    var markers = cluster.getAllChildMarkers();

    // Inicializar la suma del valor deseado
    var sum = 0;

    // Sumar el valor deseado de cada marcador
    markers.forEach(function(marker) {
        // Supongamos que el valor deseado se almacena en una propiedad 'valor' de cada marcador
        sum += marker.options.count || 0; // si 'valor' no está definido, se suma 0
    });

    // Crear el ícono del cluster con el número de suma
    return L.divIcon({
        html: '<div><span>' + sum + '</span></div>',
        className: 'leaflet-marker-icon marker-cluster marker-cluster-small leaflet-zoom-animated leaflet-interactive',
        iconSize: L.point(40, 40)
    });
}

// Crear el cluster de marcadores y configurar la opción iconCreateFunction
var markers = L.markerClusterGroup({
    iconCreateFunction: createClusterIcon
});

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
                    fillOpacity: 0.8,
                    count: doc.count
                }).bindTooltip(doc.country + ': ' + doc.count + ' documents', {permanent: true, direction: 'top'}).openTooltip();
                markers.addLayer(marker);
            });
            map.addLayer(markers);
        })
        .catch(error => console.error('Error fetching map data:', error));
}
