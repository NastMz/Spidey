// Función para actualizar la gráfica de dona
const colors = [
    '#2D3E50', '#A11A3A', '#9BA64A', '#F24131', '#0080B0'
]

function updatePieChart() {
    fetch('/api/data/charts/pie')
        .then(response => response.json())
        .then(data => {
            var pieChartDom = document.getElementById('pie-chart-container');
            var pieChart = echarts.init(pieChartDom);
            var pieOption = {
                title: {
                    text: 'Universidades por País',
                    subtext: 'Distribución',
                    left: 'center',
                    textStyle: {
                        color: '#fff'
                    },
                    subtextStyle: {
                        color: '#fff'
                    }
                },
                tooltip: {
                    trigger: 'item',

                },
                legend: {
                    top: 'bottom',
                    textStyle: {
                        color: '#fff'
                    },

                },
                series: [
                    {
                        label: {
                            color: '#717171'
                        },
                        labelLine: {
                            lineStyle: {
                                color: '#717171'
                            },
                            smooth: 0.2,
                            length: 10,
                            length2: 20
                        },
                        name: 'Universidades',
                        type: 'pie',
                        radius: '55%',
                        center: ['50%', '50%'],
                        data: data.data,
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)',
                                borderColor: '#ff6a00',
                                borderWidth: 3
                            }
                        },
                        itemStyle: {
                            normal: {
                                borderColor: '#282828',
                                borderWidth: 2,
                                color: function (params) {
                                    // Comprueba si el valor de la barra es el máximo
                                    return params.value === Math.max(...data.data.map(item => item.value)) ? '#A11A3A' : colors[params.dataIndex % colors.length];
                                }
                            }
                        }
                    }
                ]
            };
            pieChart.setOption(pieOption);
        })
        .catch(error => console.error('Error fetching pie chart data:', error));
}

// Función para actualizar la gráfica de barras
function updateBarChart() {
    fetch('/api/data/charts/bar')
        .then(response => response.json())
        .then(data => {
            var barChartDom = document.getElementById('bar-chart-container');
            var barChart = echarts.init(barChartDom);
            var barOption = {
                title: {
                    text: 'Documentos por Universidad',
                    subtext: 'Top Universidades',
                    left: 'center',
                    textStyle: {
                        color: '#fff'
                    },
                    subtextStyle: {
                        color: '#fff'
                    }
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {type: 'shadow'}
                },
                xAxis: {
                    type: 'category',
                    data: data.categories,
                    axisLabel: {
                        rotate: 45,
                        interval: 0,
                        color: '#717171',
                        fontSize: 10,
                    },
                    axisLine: {show: false},
                    splitLine: {show: false}
                },
                yAxis: {
                    type: 'value',
                    axisLabel: {show: false}, // Oculta las etiquetas del eje Y
                    axisLine: {show: false},
                    splitLine: {show: false}
                },
                series: [
                    {
                        name: 'Documentos',
                        type: 'bar',
                        data: data.data,
                        label: {
                            show: true,
                            position: 'top',
                            color: '#717171'
                        },
                        itemStyle: {
                            color: function (params) {
                                return params.dataIndex === data.data.indexOf(Math.max(...data.data)) ? '#ff6a00' : '#ffaf7c';
                            }
                        }
                    }
                ]
            };
            barChart.setOption(barOption);
        })
        .catch(error => console.error('Error fetching bar chart data:', error));
}

// Función para actualizar el gráfico Half Doughnut
function updateHalfDoughnutChart() {
    fetch('/api/data/charts/languages')
        .then(response => response.json())
        .then(data => {
            var halfDoughnutDom = document.getElementById('half-doughnut-container');
            var halfDoughnutChart = echarts.init(halfDoughnutDom);
            var halfDoughnutOption = {
                title: {
                    text: 'Distribución de Idiomas',
                    subtext: 'Documentos por Idioma',
                    left: 'center',
                    textStyle: {
                        color: '#fff'
                    },
                    subtextStyle: {
                        color: '#fff'
                    }
                },
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    top: 'bottom',
                    left: 'center',
                    textStyle: {
                        color: '#fff'
                    },
                },
                series: [
                    {
                        name: 'Documentos',
                        type: 'pie',
                        radius: ['40%', '70%'],
                        center: ['50%', '70%'],
                        startAngle: 180,
                        endAngle: 360,
                        label: {
                            show: true,
                            position: 'center',
                            formatter: '{b}\n{d}%',
                            color: '#717171'
                        },
                        itemStyle: {
                            color: function (params) {
                                // Obtener el valor máximo
                                var maxCount = Math.max(...data.data.map(item => item.count));
                                // Comparar el valor actual con el valor máximo
                                return params.data.value === maxCount ? '#ff6a00' : '#ffaf7c';
                            }
                        },
                        emphasis: {
                            label: {
                                show: true,
                                fontSize: '20',
                                fontWeight: 'bold'
                            }
                        },
                        labelLine: {
                            show: false
                        },
                        data: data.data.map(item => ({
                            value: item.count,
                            name: item.language
                        }))
                    }
                ]
            };
            halfDoughnutChart.setOption(halfDoughnutOption);
        })
        .catch(error => console.error('Error fetching half doughnut chart data:', error));
}