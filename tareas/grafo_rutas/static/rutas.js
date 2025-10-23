class SistemaRutas {
    constructor() {
        this.ciudades = {};
        this.conexiones = [];
        this.pesos = {};
        
        this.actualizarEstado("Inicializando...");
        this.cargarMapa();
    }

    actualizarEstado(mensaje) {
        const estadoElement = document.getElementById('estado');
        if (estadoElement) {
            estadoElement.textContent = mensaje;
        }
    }

    actualizarContadores() {
        const ciudadesElement = document.getElementById('contador-ciudades');
        const rutasElement = document.getElementById('contador-rutas');
        
        if (ciudadesElement) {
            ciudadesElement.textContent = Object.keys(this.ciudades).length;
        }
        if (rutasElement) {
            rutasElement.textContent = this.conexiones.length;
        }
    }

    async cargarMapa() {
        try {
            this.actualizarEstado("Cargando datos del mapa...");
            
            const response = await fetch('/api/mapa');
            
            if (!response.ok) {
                throw new Error(`Error del servidor: ${response.status}`);
            }
            
            const data = await response.json();
            
            this.ciudades = data.ciudades || {};
            this.conexiones = data.conexiones || [];
            this.pesos = data.pesos || {};
            
            this.actualizarEstado("Datos cargados correctamente");
            this.actualizarContadores();
            
            // Actualizar interfaz
            this.actualizarSelects();
            this.mostrarListaCiudades();
            this.dibujarMapa();
            
            document.getElementById('resultado').innerHTML = 
                '✅ <strong>Mapa cargado correctamente:</strong> ' + 
                Object.keys(this.ciudades).length + ' ciudades y ' + 
                this.conexiones.length + ' rutas';
            
        } catch (error) {
            this.actualizarEstado("Error cargando mapa");
            document.getElementById('resultado').innerHTML = 
                '❌ <strong>Error:</strong> ' + error.message;
        }
    }

    actualizarSelects() {
        const origen = document.getElementById('origen');
        const destino = document.getElementById('destino');
        
        origen.innerHTML = '<option value="">Ciudad Origen</option>';
        destino.innerHTML = '<option value="">Ciudad Destino</option>';

        Object.keys(this.ciudades).forEach(ciudad => {
            origen.innerHTML += `<option value="${ciudad}">${ciudad}</option>`;
            destino.innerHTML += `<option value="${ciudad}">${ciudad}</option>`;
        });
    }

    mostrarListaCiudades() {
        const lista = document.getElementById('lista-ciudades');
        lista.innerHTML = '';
        
        Object.keys(this.ciudades).forEach(ciudad => {
            const div = document.createElement('div');
            div.textContent = `• ${ciudad}`;
            div.style.padding = '2px 0';
            lista.appendChild(div);
        });
    }

    dibujarMapa() {
        this.actualizarEstado("Dibujando mapa...");
        this.dibujarRutas();
        this.dibujarCiudades();
        this.actualizarEstado("Mapa listo");
    }

    dibujarCiudades() {
        const ciudadesGroup = document.getElementById('ciudades');
        ciudadesGroup.innerHTML = '';

        Object.entries(this.ciudades).forEach(([nombre, [x, y]]) => {
            const grupo = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            grupo.setAttribute('class', 'ciudad');
            grupo.setAttribute('id', `ciudad-${nombre}`);

            // Círculo de la ciudad
            const circulo = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circulo.setAttribute('cx', x);
            circulo.setAttribute('cy', y);
            circulo.setAttribute('r', 12);
            circulo.setAttribute('class', 'circulo-ciudad');
            circulo.setAttribute('id', `circulo-${nombre}`);

            // Nombre de la ciudad
            const texto = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            texto.setAttribute('x', x);
            texto.setAttribute('y', y - 18);
            texto.setAttribute('class', 'nombre-ciudad');
            texto.setAttribute('text-anchor', 'middle');
            texto.textContent = nombre;

            grupo.appendChild(circulo);
            grupo.appendChild(texto);
            ciudadesGroup.appendChild(grupo);
        });
    }

    dibujarRutas() {
        const rutasGroup = document.getElementById('rutas');
        rutasGroup.innerHTML = '';

        this.conexiones.forEach(([ciudad1, ciudad2]) => {
            const coord1 = this.ciudades[ciudad1];
            const coord2 = this.ciudades[ciudad2];
            
            if (!coord1 || !coord2) {
                return;
            }
            
            // Buscar el peso
            let peso = null;
            const posiblesClaves = [
                `${ciudad1}-${ciudad2}`,
                `${ciudad2}-${ciudad1}`
            ];
            
            for (const clave of posiblesClaves) {
                if (this.pesos[clave] !== undefined) {
                    peso = this.pesos[clave];
                    break;
                }
            }
            
            if (peso === null) {
                peso = "?";
            }

            // Línea de la ruta
            const linea = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            linea.setAttribute('x1', coord1[0]);
            linea.setAttribute('y1', coord1[1]);
            linea.setAttribute('x2', coord2[0]);
            linea.setAttribute('y2', coord2[1]);
            linea.setAttribute('class', 'ruta');
            linea.setAttribute('id', `ruta-${ciudad1}-${ciudad2}`);

            // Texto del peso
            if (peso !== "?") {
                const texto = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                const midX = (coord1[0] + coord2[0]) / 2;
                const midY = (coord1[1] + coord2[1]) / 2;
                
                texto.setAttribute('x', midX);
                texto.setAttribute('y', midY - 8);
                texto.setAttribute('class', 'peso-ruta');
                texto.setAttribute('text-anchor', 'middle');
                texto.textContent = peso;

                rutasGroup.appendChild(texto);
            }
            
            rutasGroup.appendChild(linea);
        });
    }

    async calcularRuta() {
        const origen = document.getElementById('origen').value;
        const destino = document.getElementById('destino').value;

        if (!origen || !destino) {
            alert('Por favor selecciona una ciudad de origen y una de destino');
            return;
        }

        if (origen === destino) {
            alert('Por favor selecciona ciudades diferentes para origen y destino');
            return;
        }

        this.actualizarEstado("Calculando ruta óptima...");
        this.limpiarAnimaciones();

        try {
            const response = await fetch('/api/ruta', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ origen, destino })
            });

            const resultado = await response.json();
            
            if (resultado.status === 'success') {
                // Mostrar animación del algoritmo
                await this.animarDijkstra(resultado.pasos);
                
                // Dibujar ruta óptima
                this.dibujarRutaOptima(resultado.camino);
                
                document.getElementById('resultado').innerHTML = 
                    `<strong>✅ Ruta Óptima Encontrada:</strong><br>
                     <strong>📍 Recorrido:</strong> ${resultado.camino.join(' → ')}<br>
                     <strong>📏 Distancia Total:</strong> ${resultado.distancia} km`;
                
                this.actualizarEstado("Ruta calculada correctamente");
            } else {
                document.getElementById('resultado').innerHTML = 
                    `<strong>❌ Error:</strong> ${resultado.message}`;
                this.actualizarEstado("Error en cálculo de ruta");
            }
                 
        } catch (error) {
            document.getElementById('resultado').innerHTML = 
                '<strong>❌ Error:</strong> No se pudo conectar con el servidor';
            this.actualizarEstado("Error de conexión");
        }
    }

    async animarDijkstra(pasos) {
        this.actualizarEstado("Animando algoritmo Dijkstra...");
        
        for (let i = 0; i < pasos.length; i++) {
            const [accion, ciudad, valor] = pasos[i];
            
            await new Promise(resolve => setTimeout(resolve, 300)); // Pausa de 300ms
            
            const circulo = document.getElementById(`circulo-${ciudad}`);
            if (circulo) {
                if (accion === 'visitando') {
                    circulo.style.fill = '#ffd700'; // Amarillo - visitando
                    circulo.style.stroke = '#ff6b00';
                } else if (accion === 'actualizando') {
                    circulo.style.fill = '#90ee90'; // Verde claro - actualizando
                    circulo.style.stroke = '#28a745';
                }
            }
        }
        
        // Restaurar colores después de la animación
        setTimeout(() => {
            this.limpiarAnimaciones();
        }, 1000);
    }

    limpiarAnimaciones() {
        // Restaurar colores originales de todas las ciudades
        Object.keys(this.ciudades).forEach(ciudad => {
            const circulo = document.getElementById(`circulo-${ciudad}`);
            if (circulo) {
                circulo.style.fill = '#d52b1e';
                circulo.style.stroke = '#fdda00';
            }
        });
    }

    dibujarRutaOptima(camino) {
        const rutaGroup = document.getElementById('ruta-calculada');
        rutaGroup.innerHTML = '';

        for (let i = 0; i < camino.length - 1; i++) {
            const ciudad1 = camino[i];
            const ciudad2 = camino[i + 1];
            
            const coord1 = this.ciudades[ciudad1];
            const coord2 = this.ciudades[ciudad2];

            if (coord1 && coord2) {
                const linea = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                linea.setAttribute('x1', coord1[0]);
                linea.setAttribute('y1', coord1[1]);
                linea.setAttribute('x2', coord2[0]);
                linea.setAttribute('y2', coord2[1]);
                linea.setAttribute('class', 'ruta-optima');

                rutaGroup.appendChild(linea);
            }
        }
    }

    limpiarRuta() {
        document.getElementById('ruta-calculada').innerHTML = '';
        this.limpiarAnimaciones();
        document.getElementById('resultado').innerHTML = 
            '✅ <strong>Mapa listo:</strong> ' + 
            Object.keys(this.ciudades).length + ' ciudades y ' + 
            this.conexiones.length + ' rutas cargadas';
        this.actualizarEstado("Listo");
    }
}

// Inicializar cuando cargue la página
document.addEventListener('DOMContentLoaded', () => {
    window.sistemaRutas = new SistemaRutas();
});

// Funciones globales para los botones
function calcularRuta() {
    window.sistemaRutas.calcularRuta();
}

function limpiarRuta() {
    window.sistemaRutas.limpiarRuta();
}