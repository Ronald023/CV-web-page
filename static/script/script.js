document.addEventListener('DOMContentLoaded', function() {

    // --- 1. DEFINE TUS DATOS DE LA LÍNEA DE TIEMPO ---
    // Aquí puedes agregar toda tu experiencia y educación.
    // 'type' puede ser 'work' o 'education' para usar diferentes íconos.
    const timelineData = [
        {
            type: 'education',
            title: 'Programación Básica',
            organization: 'Talento Tech Oriente',
            date: '2025',
            description: 'Curso intensivo sobre los fundamentos de la programación, incluyendo algoritmos, estructuras de datos, y desarrollo web con HTML, CSS y JavaScript.'
        },
        {
            type: 'education',
            title: 'Matemático (en curso)',
            organization: 'Universidad Industrial de Santander',
            date: '2021 - Presente',
            description: 'Estudios en matemáticas puras y aplicadas, con un fuerte enfoque en lógica, cálculo avanzado y modelado estadístico. Habilidades desarrolladas en resolución de problemas complejos y pensamiento analítico.'
        },
        {
            type: 'work',
            title: 'Puesto Anterior',
            organization: 'Otra Empresa',
            date: '2018 - 2020',
            description: '<li>Descripción de funciones realizadas.</li><li>Proyecto importante completado.</li><li>Habilidad clave desarrollada.</li>'
        },
        {
            type: 'work',
            title: 'Trabajo Actual',
            organization: 'Nombre de la Empresa',
            date: '2020 - Presente',
            description: '<ul><li>Rol y responsabilidades principales.</li><li>Logro destacado: optimización de procesos que resultó en un X% de mejora.</li><li>Tecnologías utilizadas: JavaScript, React, Node.js.</li></ul>'
        },
        // ¡Agrega más eventos aquí!
    ];

    // --- 2. GENERA LA LÍNEA DE TIEMPO DINÁMICAMENTE ---
    const timelineContainer = document.getElementById('interactive-timeline');

    timelineData.forEach(event => {
        // Crear el contenedor principal del evento
        const eventElement = document.createElement('div');
        eventElement.classList.add('timeline-event');

        // Determinar el ícono basado en el tipo de evento
        const iconClass = event.type === 'work' ? 'fa-briefcase' : 'fa-graduation-cap';

        // Usamos innerHTML para construir la estructura interna fácilmente
        eventElement.innerHTML = `
            <div class="timeline-point">
                <i class="fas ${iconClass}"></i>
            </div>
            <div class="timeline-body">
                <div class="timeline-header">
                    <h3>${event.title}</h3>
                    <span class="timeline-date">${event.date}</span>
                </div>
                <span class="timeline-company">${event.organization}</span>
                <div class="timeline-content">
                    <p>${event.description}</p>
                </div>
            </div>
        `;

        timelineContainer.appendChild(eventElement);
    });

    // --- 3. AÑADE LA INTERACTIVIDAD (EVENT LISTENERS) ---
    const allEvents = document.querySelectorAll('.timeline-event');

    allEvents.forEach(event => {
        // Hacemos que tanto el punto como el encabezado sean clickeables
        const clickablePoint = event.querySelector('.timeline-point');
        const clickableHeader = event.querySelector('.timeline-header');

        const toggleActive = () => {
            // Si el evento ya está activo, lo cerramos
            if (event.classList.contains('active')) {
                event.classList.remove('active');
            } else {
                // Si no, cerramos cualquier otro que esté abierto
                allEvents.forEach(el => el.classList.remove('active'));
                // Y abrimos el actual
                event.classList.add('active');
            }
        };
        
        clickablePoint.addEventListener('click', toggleActive);
        clickableHeader.addEventListener('click', toggleActive);
    });

    // Opcional: Abrir el primer evento por defecto
    if (allEvents.length > 0) {
        allEvents[0].classList.add('active');
    }

});

