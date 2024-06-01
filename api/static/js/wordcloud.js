function updateTreemap() {
    fetch('/api/data/charts/treemap')
        .then(response => response.json())
        .then(data => {
            var chartDom = document.getElementById('treemap-container');
            var myChart = echarts.init(chartDom);
            var option;
            option = {
                title: {
                    text: 'Top 30 most frequent words',
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
                        data: data.data[0].children.slice(0, 30),
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
    fetch('/api/data/charts/treemap')
        .then(response => response.json())
        .then(data => {
            const totalValue = data.data[0].children.length;
            animateNumber("indicator-words", totalValue, 3000);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function createWordCloud() {
    fetch('/api/data/bag_of_words')
        .then(response => response.json())
        .then(data => {
            // Convertir y ordenar palabras por frecuencia
            const words = Object.entries(data.words)
                .map(([key, value]) => ({text: key, frequency: value}))
                .sort((a, b) => b.frequency - a.frequency)
                .slice(0, 80);  // Tomar las primeras 50 palabras

            const svg = d3.select("#wordcloud");
            const container = document.getElementById('wordcloud-container');

            // Obtener dimensiones dinámicas del contenedor
            const width = container.clientWidth;
            const height = container.clientHeight;

            const wordScale = d3.scaleLinear()
                .domain([d3.min(words, d => d.frequency), d3.max(words, d => d.frequency)])
                .range([20, 80]);  // Ajustar el rango para reducir el tamaño máximo

            function draw(words) {
                svg.attr("width", width)
                    .attr("height", height);

                const g = svg.append("g")
                    .attr("transform", `translate(${width / 2}, ${height / 2})`);

                g.selectAll("text")
                    .data(words)
                    .enter().append("text")
                    .style("font-size", d => `${d.size}px`)
                    .style("fill", d => colors[Math.floor(Math.random() * colors.length)])
                    .attr("text-anchor", "middle")
                    .attr("transform", d => `translate(${d.x}, ${d.y})rotate(${d.rotate})`)
                    .text(d => d.text);
            }

            d3.layout.cloud()
                .size([width, height])
                .words(words)
                .rotate(() => 0)
                .fontSize(d => wordScale(d.frequency))
                .padding(5)  // Aumentar el padding para reducir el cruce
                .on("end", draw)
                .start();
        })
        .catch(error => console.error('Error fetching word data:', error));
}
