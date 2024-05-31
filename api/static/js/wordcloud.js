function updateTreemap() {
    fetch('/api/data/charts/treemap')
        .then(response => response.json())
        .then(data => {
            var chartDom = document.getElementById('treemap-container');
            var myChart = echarts.init(chartDom);
            var option;
            console.log(data.data[0].children.slice(0,30))
            option = {
                title: {
                    text: 'Top Palabras Más Repetitivas',
                    left: 'center',
                    textStyle: {
                        color: '#fff'
                    }
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{b}: {c}'
                },
                series: [
                    {
                        type: 'treemap',
                        data: data.data[0].children.slice(0,30),
                        leafDepth: 1,
                        label: {
                            show: true,
                            formatter: '{b}',
                            color: '#fff'
                        },
                        itemStyle: {
                            borderColor: '#fff'
                        },
                        levels: [
                            {
                                itemStyle: {
                                    borderWidth: 1,
                                    gapWidth: 1
                                }
                            },
                            {
                                colorSaturation: [0.3, 0.6],
                                itemStyle: {
                                    gapWidth: 1,
                                    borderColorSaturation: 0.7
                                }
                            }
                        ]
                    }
                ]
            };

            option && myChart.setOption(option);
        })
        .catch(error => console.error('Error fetching treemap data:', error));
}
// Función para contar el total de palabras
function countTotalWords() {
   fetch('http://localhost:5000/api/data/charts/treemap')
        .then(response => response.json())
        .then(data => {
            const totalValue = data.data[0].children.reduce((acc, child) => acc + child.value, 0);
            console.log('Total Value:', totalValue);
            document.getElementById('indicator-words').textContent = totalValue;
        })
        .catch(error => console.error('Error fetching data:', error));
}
