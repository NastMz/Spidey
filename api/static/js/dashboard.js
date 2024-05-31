// Función para desplazar la página hacia arriba o hacia abajo
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

// Llamar a las funciones para actualizar los indicadores y las gráficas al cargar la página
document.addEventListener('DOMContentLoaded', function () {
    updateIndicators();
    updatePieChart();
    updateBarChart();
    updateHalfDoughnutChart();
    updateMap();
    countTotalWords();
    updateTreemap();
});