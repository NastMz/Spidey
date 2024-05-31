document.addEventListener("DOMContentLoaded", function () {
    var chartDom = document.getElementById('globe-container');
    var myChart = echarts.init(chartDom);
    var option;
    // Datos de los países
    var countriesData = [
        {
            "country": "Chile",
            "coords": [
                -31.7613365,
                -71.3187697
            ]
        },
        {
            "country": "France",
            "coords": [
                46.603354,
                1.8883335
            ]
        },
        {
            "country": "United States",
            "coords": [
                39.7837304,
                -100.445882
            ]
        },
        {
            "country": "Thailand",
            "coords": [
                7.4931858,
                124.724704
            ]
        },
        {
            "country": "Brasil",
            "coords": [
                -10.3333333,
                -53.2
            ]
        },
        {
            "country": "Germany",
            "coords": [
                51.1638175,
                10.4478313
            ]
        },
        {
            "country": "New Zealand",
            "coords": [
                -41.5000831,
                172.8344077
            ]
        },
        {
            "country": "Australia",
            "coords": [
                -24.7761086,
                134.755
            ]
        },
        {
            "country": "United Kingdom",
            "coords": [
                54.7023545,
                -3.2765753
            ]
        },
        {
            "country": "Spain",
            "coords": [
                39.3260685,
                -4.8379791
            ]
        },
        {
            "country": "Colombia",
            "coords": [
                4.099917,
                -72.9088133
            ]
        },
        {
            "country": "Japan",
            "coords": [
                36.5748441,
                139.2394179
            ]
        },
        {
            "country": "Canada",
            "coords": [
                61.0666922,
                -107.991707
            ]
        },
        {
            "country": "China",
            "coords": [
                35.000074,
                104.999927
            ]
        },
        {
            "country": "Singapore",
            "coords": [
                1.357107,
                103.8194992
            ]
        }
    ];

// Generar array de líneas
    var lineData = [];

    for (var i = 0; i < countriesData.length; i++) {
        for (var j = i + 1; j < countriesData.length; j++) {
            var coords1 = countriesData[i].coords;
            var coords2 = countriesData[j].coords;

            lineData.push({
                coords: [coords1, coords2],
                lineStyle: {
                    color: 'rgb(50, 50, 150)',
                    opacity: 0.8
                }
            });
        }
    }

    // Generar array de puntos
    var pointData = [];

// Agregar los orígenes
    for (var i = 0; i < countriesData.length; i++) {
        pointData.push({
            name: countriesData[i].country,
            value: countriesData[i].coords
        });
    }

    option = {
        globe: {
            baseTexture: '/static/img/worldmap (1).png',
            shading: 'lambert',
            atmosphere: {
                show: true,
                color: 'rgb(99,130,239)',
                glowPower: 6
            },
            light: {
                ambient: {
                    intensity: 0.1
                },
                main: {
                    intensity: 1.5
                }
            },
            viewControl: {
                autoRotate: true,
                autoRotateAfterStill: 10,
                distance: 250,
            }
        },
        series: [{
            type: 'lines3D',
            coordinateSystem: 'globe',
            effect: {
                show: true,
                trailWidth: 2,
                trailOpacity: 0.8,
                trailLength: 0.2,
                constantSpeed: 40
            },
            blendMode: 'lighter',
            lineStyle: {
                width: 2,
                color: '#fff',
                opacity: 0.6
            },
            data: lineData
        },
            {
                type: 'scatter3D',
                coordinateSystem: 'globe',
                blendMode: 'lighter',
                symbolSize: 10,
                itemStyle: {color: 'rgb(50, 50, 150)', opacity: 0.8},
                data: pointData
            }]
    };

    myChart.setOption(option);
});
