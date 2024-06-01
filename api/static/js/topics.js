async function countTotalTopics() {
    try {
        const response = await fetch('/api/model/topics');
        const data = await response.json();
        return data.data.length;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

async function fetchTopicDetails(topicId) {
    try {
        const response = await fetch(`/api/model/topics/${topicId}`);
        const data = await response.json();
        return data.words;
    } catch (error) {
        console.error('Error fetching topic details:', error);
    }
}

async function initialize() {
    const totalTopics = await countTotalTopics();
    animateNumber("indicator-topic", totalTopics, 3000);
    const topicSelector = document.getElementById('topicSelector');

    // Populate the topic selector with optionsindicator-topic
    for (let i = 0; i < 30; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.text = `Topic ${i + 1}`;
        topicSelector.appendChild(option);
    }

    // Initialize the chart
    const chart = echarts.init(document.getElementById('chart'));
    const initialData = await fetchTopicDetails(0);
    updateChart(chart, initialData);

    // Add event listener to update the chart based on selected topic
    topicSelector.addEventListener('change', async function () {
        const selectedTopic = topicSelector.value;
        const topicData = await fetchTopicDetails(selectedTopic);
        updateChart(chart, topicData);
    });
}

function updateChart(chart, data) {
    const words = data.map(item => item.word);
    const probabilities = data.map(item => item.probability);

    // Encontrar el índice del valor mayor
    const maxIndex = probabilities.indexOf(Math.max(...probabilities));

    // Asignar colores según el valor
    const barColors = probabilities.map((_, index) => index === maxIndex ? '#ff6a00' : '#ffaf7c');

    const option = {
        title: {
            text: 'Word Probabilities',
            textStyle: {
                color: '#fff'
            },
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {type: 'shadow'}
        },
        xAxis: {
            type: 'category',
            data: words,
            axisLabel: {
                rotate: 45,
                interval: 0,
                color: '#717171',
                fontSize: 10,
            },
        },
        yAxis: {
            type: 'value',
        },
        series: [{
            type: 'bar',
            data: probabilities,
            itemStyle: {
                color: function (params) {
                    return barColors[params.dataIndex];
                }
            },
        }],
    };

    chart.setOption(option);
}

function updateInteropicChart() {
    fetch('/api/model/intertopic')
        .then(response => response.json())
        .then(data => {

            const topicdata = data.data.slice(0, 30);

            const seriesData = topicdata.map(item => ({
                value: [item.coordinates[0], item.coordinates[1], item.size / 50, item.words],
                name: item.topic
            }))

            seriesData.sort((a, b) => b.value[2] - a.value[2]);

            var chartDom = document.getElementById('intertopic-container');
            var myChart = echarts.init(chartDom);

            const option = {
                title: {
                    text: 'Intertopic Distance Visualization - 30 First Topics',
                    textStyle: {
                        color: '#fff'
                    }
                },
                tooltip: {
                    trigger: 'item',
                    formatter: function (params) {
                        return `Topic: ${params.name}<br/>Size: ${params.value[2]}<br/>Words: ${params.value[3]}`;
                    }
                },
                xAxis: {
                    name: 'UMAP Dimension 1'
                },
                yAxis: {
                    name: 'UMAP Dimension 2'
                },
                series: [{
                    type: 'scatter',
                    data: seriesData,
                    symbolSize: function (data) {
                        return data[2]; // Utiliza el tamaño del punto basado en el valor de 'Size'
                    },
                    itemStyle: {
                        opacity: 0.6,
                        borderColor: '#fff',
                        borderWidth: 0.5,
                        color: '#ff8e48'
                    },
                    emphasis: {
                        itemStyle: {
                            color: '#ff6a00'
                        }
                    }
                }]
            };

            option && myChart.setOption(option);
        })
        .catch(error => console.error('Error fetching treemap data:', error));
}

document.getElementById('textForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission

    const text = document.getElementById('textInput').value;

    fetch('http://127.0.0.1:5000/api/model/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({text: text})
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('probability').textContent = data.probability;
            document.getElementById('topic').textContent = data.topic;
        })
        .catch(error => console.error('Error:', error));
});



