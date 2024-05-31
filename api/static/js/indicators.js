// Función para actualizar los indicadores
function updateIndicators() {
    fetch('/api/data/indicators')
        .then(response => response.json())
        .then(data => {
            // Llamar a la función para animar los números con los valores deseados
            animateNumber("indicator-countries", data.countries, 2000); // Ejemplo con 15 como valor final y 2000 ms de duración
            animateNumber("indicator-universities", data.universities, 2000); // Ejemplo con 25 como valor final y 2000 ms de duración
            animateNumber("indicator-docs", data.docs, 2000); // Ejemplo con 100 como valor final y 2000 ms de duración
            animateNumber("indicator-languages", 2, 2000); // Ejemplo con 5 como valor final y 2000 ms de duración

        })
        .catch(error => console.error('Error fetching indicators:', error));
}

// Función para animar el incremento de números
function animateNumber(elementId, finalNumber, duration) {
    var element = document.getElementById(elementId);
    var startNumber = parseInt(element.innerText);
    var increment = finalNumber - startNumber;
    var startTime = null;

    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        var progress = timestamp - startTime;
        var percentage = Math.min(progress / duration, 1);
        element.innerText = Math.floor(startNumber + increment * percentage);

        if (progress < duration) {
            window.requestAnimationFrame(step);
        }
    }

    window.requestAnimationFrame(step);
}