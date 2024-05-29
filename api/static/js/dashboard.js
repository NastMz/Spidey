// Inicializar el mapa
var map = L.map('map').setView([0, 0], 2); // Coordenadas iniciales y nivel de zoom
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Ejemplo de documentos por país con coordenadas
var documents = [
    {country: 'USA', coords: [37.0902, -95.7129], count: 1048},
    {country: 'China', coords: [35.8617, 104.1954], count: 735},
    {country: 'Canada', coords: [56.1304, -106.3468], count: 580},
    {country: 'UK', coords: [55.3781, -3.4360], count: 484},
    {country: 'Germany', coords: [51.1657, 10.4515], count: 300}
];

documents.forEach(function (doc) {
    L.circleMarker(doc.coords, {
        radius: 10,
        fillColor: "#0078FF",
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
    }).addTo(map)
        .bindTooltip(doc.count + ' documentos', {permanent: true, direction: 'top'})
        .openTooltip();
});

// Inicializar ECharts - Gráfica de dona
var pieChartDom = document.getElementById('pie-chart-container');
var pieChart = echarts.init(pieChartDom);
var pieOption;

pieOption = {
    title: {
        text: 'Universidades por Continente',
        subtext: 'Distribución',
        left: 'center'
    },
    tooltip: {
        trigger: 'item'
    },
    legend: {
        top: 'bottom'
    },
    series: [
        {
            name: 'Universidades',
            type: 'pie',
            radius: '50%',
            data: [
                {value: 300, name: 'Asia'},
                {value: 200, name: 'Europa'},
                {value: 150, name: 'América del Norte'},
                {value: 100, name: 'América del Sur'},
                {value: 50, name: 'África'}
            ],
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)',
                    borderColor: '#FFD700',
                    borderWidth: 3
                }
            },
            itemStyle: {
                normal: {
                    borderColor: '#FFF',
                    borderWidth: 2,
                    color: function (params) {
                        // Resaltar el continente con más universidades (Asia en este caso)
                        return params.name === 'Asia' ? '#FF6347' : '#0078FF';
                    }
                }
            }
        }
    ]
};

pieOption && pieChart.setOption(pieOption);

// Inicializar ECharts - Gráfica de barras
var barChartDom = document.getElementById('bar-chart-container');
var barChart = echarts.init(barChartDom);
var barOption;

barOption = {
    title: {
        text: 'Documentos por Universidad',
        subtext: 'Top Universidades',
        left: 'center'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {type: 'shadow'}
    },
    xAxis: {
        type: 'category',
        data: ['Universidad A', 'Universidad B', 'Universidad C', 'Universidad D', 'Universidad E']
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name: 'Documentos',
            type: 'bar',
            data: [120, 200, 150, 80, 70],
            itemStyle: {
                color: function (params) {
                    // Resaltar la universidad con más documentos (Universidad B en este caso)
                    return params.dataIndex === 1 ? '#FF6347' : '#0078FF';
                }
            }
        }
    ]
};

barOption && barChart.setOption(barOption);

function scrollUpDown() {
    var scrollIcon = document.getElementById('scroll-icon');
    var isScrollDown = scrollIcon.classList.contains('fa-caret-down');

    if (isScrollDown) {
        window.scrollBy({
            top: window.innerHeight,
            behavior: 'smooth'
        });
        scrollIcon.classList.remove('fa-caret-down');
        scrollIcon.classList.add('fa-caret-up');
    } else {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
        scrollIcon.classList.remove('fa-caret-up');
        scrollIcon.classList.add('fa-caret-down');
    }
}

// Obtén los elementos contenedores de los gráficos
var wordCloudContainer = document.getElementById('word-cloud');
var treemapContainer = document.getElementById('treemap');

// Inicializa los gráficos de ECharts en los contenedores correspondientes
var wordCloudChart = echarts.init(wordCloudContainer);
var treemapChart = echarts.init(treemapContainer);

// Datos de ejemplo para la nube de palabras y el treemap
var wordCloudData = [
    { name: 'Word1', value: 100 },
    { name: 'Word2', value: 80 },
    { name: 'Word3', value: 60 },
    // Agrega más datos de ejemplo según sea necesario
];

var treemapData = [
    { name: 'Category1', value: 100, children: [
        { name: 'Subcategory1', value: 50 },
        { name: 'Subcategory2', value: 30 },
        // Agrega más subcategorías según sea necesario
    ]},
    { name: 'Category2', value: 80, children: [
        { name: 'Subcategory3', value: 40 },
        { name: 'Subcategory4', value: 20 },
        // Agrega más subcategorías según sea necesario
    ]},
    // Agrega más categorías según sea necesario
];

// Configuración de la nube de palabras
var wordCloudOption = {
    series: [{
        type: 'wordCloud',
        data: wordCloudData
    }]
};

// Configuración del treemap
var treemapOption = {
    series: [{
        type: 'treemap',
        data: treemapData
    }]
};

// Establece las opciones y renderiza los gráficos
wordCloudOption && wordCloudChart.setOption(wordCloudOption);
treemapOption && treemapChart.setOption(treemapOption);
// Obtén los elementos contenedores de los gráficos
var wordCloudContainer = document.getElementById('word-cloud');
var treemapContainer = document.getElementById('treemap');

// Inicializa los gráficos de ECharts en los contenedores correspondientes
var wordCloudChart = echarts.init(wordCloudContainer);
var treemapChart = echarts.init(treemapContainer);

// Datos de ejemplo para la nube de palabras y el treemap
var wordCloudData = [
    { name: 'Word1', value: 100 },
    { name: 'Word2', value: 80 },
    { name: 'Word3', value: 60 },
    // Agrega más datos de ejemplo según sea necesario
];

var treemapData = [
    { name: 'Category1', value: 100, children: [
        { name: 'Subcategory1', value: 50 },
        { name: 'Subcategory2', value: 30 },
        // Agrega más subcategorías según sea necesario
    ]},
    { name: 'Category2', value: 80, children: [
        { name: 'Subcategory3', value: 40 },
        { name: 'Subcategory4', value: 20 },
        // Agrega más subcategorías según sea necesario
    ]},
    // Agrega más categorías según sea necesario
];

// Configuración de la nube de palabras
var wordCloudOption = {
    series: [{
        type: 'wordCloud',
        data: wordCloudData
    }]
};

// Configuración del treemap
var treemapOption = {
    series: [{
        type: 'treemap',
        data: treemapData
    }]
};

// Establece las opciones y renderiza los gráficos
wordCloudOption && wordCloudChart.setOption(wordCloudOption);
treemapOption && treemapChart.setOption(treemapOption);

