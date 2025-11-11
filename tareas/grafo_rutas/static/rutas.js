/*
static/rutas.js

Autor: Lorgio Añez J.
Fecha: 2025-10-23

Descripción: 
El archivo rutas.js es el principal archivo JavaScript del frontend del proyecto.
Conecta la interfaz gráfica con el backend, permitiendo que el usuario interactúe
visualmente y en tiempo real con la mapa de ciudades y sus rutas.
*/

class SistemaRutas {
    constructor() {
        this.ciudades = {};
        this.conexiones = [];
        this.pesos = {};
        this.criterioActual = 'distancia';
        
        this.actualizarEstado("Inicializando...");
        this.configurarFormularios();
        this.configurarClicksMapa(); 
        this.configurarCriterios();
        this.cargarMapa();
    }



    configurarCriterios() {
        document.querySelectorAll('.btn-criterio').forEach(btn => {
            btn.addEventListener('click', (event) => {
                document.querySelectorAll('.btn-criterio').forEach(b => b.classList.remove('active'));
                event.target.classList.add('active');
                this.criterioActual = event.target.dataset.criterio;
                
                // ✅ ACTUALIZAR EL MAPA INMEDIATAMENTE
                this.actualizarEstado(`Mostrando ${this.criterioActual === 'distancia' ? 'distancias (km)' : 'tiempos (horas)'}`);
                this.dibujarRutas(); // ← REDIBUJAR RUTAS CON NUEVO CRITERIO
                
                // ✅ ACTUALIZAR LISTA DE RUTAS TAMBIÉN
                this.mostrarListaRutas();
            });
        });
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

    configurarFormularios() {
        const formCiudad = document.getElementById('form-ciudad');
        if (formCiudad) {
            formCiudad.addEventListener('submit', (event) => {
                event.preventDefault();
                this.agregarCiudad();
            });
        }

        const formRuta = document.getElementById('form-ruta');
        if (formRuta) {
            formRuta.addEventListener('submit', (event) => {
                event.preventDefault();
                this.agregarRuta();
            });
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
            
            this.actualizarSelects();
            this.mostrarListaCiudades();
            this.mostrarListaRutas();
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
        const ciudad1Ruta = document.getElementById('ciudad1-ruta');
        const ciudad2Ruta = document.getElementById('ciudad2-ruta');
        
        if (origen) origen.innerHTML = '<option value="">Origen</option>';
        if (destino) destino.innerHTML = '<option value="">Destino</option>';
        if (ciudad1Ruta) ciudad1Ruta.innerHTML = '<option value="">Origen</option>';
        if (ciudad2Ruta) ciudad2Ruta.innerHTML = '<option value="">Destino</option>';

        Object.keys(this.ciudades).forEach(ciudad => {
            if (origen) origen.innerHTML += `<option value="${ciudad}">${ciudad}</option>`;
            if (destino) destino.innerHTML += `<option value="${ciudad}">${ciudad}</option>`;
            if (ciudad1Ruta) ciudad1Ruta.innerHTML += `<option value="${ciudad}">${ciudad}</option>`;
            if (ciudad2Ruta) ciudad2Ruta.innerHTML += `<option value="${ciudad}">${ciudad}</option>`;
        });
    }

    mostrarListaCiudades() {
        const lista = document.getElementById('lista-ciudades');
        lista.innerHTML = '';
        
        const ciudadesOrdenadas = Object.keys(this.ciudades).sort();
        
        ciudadesOrdenadas.forEach(ciudad => {
            const div = document.createElement('div');
            div.className = 'ciudad-item';
            div.innerHTML = `
                <span>• ${ciudad}</span>
                <button onclick="window.sistemaRutas.eliminarCiudad('${ciudad}')" 
                        class="btn-eliminar">🗑️</button>
            `;
            div.style.display = 'flex';
            div.style.justifyContent = 'space-between';
            div.style.alignItems = 'center';
            div.style.padding = '5px 0';
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

            const circulo = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circulo.setAttribute('cx', x);
            circulo.setAttribute('cy', y);
            circulo.setAttribute('r', '16');
            circulo.setAttribute('class', 'circulo-ciudad');
            circulo.setAttribute('id', `circulo-${nombre}`);
            circulo.setAttribute('fill', '#4745b1');
            circulo.setAttribute('stroke', '#260829');
            circulo.setAttribute('stroke-width', '3');

            const texto = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            texto.setAttribute('x', x);
            texto.setAttribute('y', y - 25);
            texto.setAttribute('class', 'nombre-ciudad');
            texto.setAttribute('text-anchor', 'middle');
            texto.setAttribute('fill', '#0c330e');
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
            
            if (!coord1 || !coord2) return;
            
            // ✅ BUSCAR PESO SEGÚN CRITERIO ACTUAL
            let peso = null;
            const posiblesClaves = [
                `${ciudad1}-${ciudad2}`,
                `${ciudad2}-${ciudad1}`
            ];
            
            for (const clave of posiblesClaves) {
                if (this.pesos[clave] !== undefined) {
                    // ✅ SI ES DICCIONARIO (con distancia/tiempo), USAR CRITERIO ACTUAL
                    if (typeof this.pesos[clave] === 'object') {
                        peso = this.pesos[clave][this.criterioActual] || this.pesos[clave]['distancia'];
                    } else {
                        // ✅ SI ES NÚMERO (viejo formato), usar directamente
                        peso = this.pesos[clave];
                    }
                    break;
                }
            }
            
            if (peso === null) {
                peso = "?";
            }

            // Dibujar línea
            const linea = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            linea.setAttribute('x1', coord1[0]);
            linea.setAttribute('y1', coord1[1]);
            linea.setAttribute('x2', coord2[0]);
            linea.setAttribute('y2', coord2[1]);
            linea.setAttribute('class', 'ruta');
            linea.setAttribute('id', `ruta-${ciudad1}-${ciudad2}`);
            
            rutasGroup.appendChild(linea);

            // Dibujar texto con peso
            if (peso !== "?") {
                const texto = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                const midX = (coord1[0] + coord2[0]) / 2;
                const midY = (coord1[1] + coord2[1]) / 2;
                
                texto.setAttribute('x', midX);
                texto.setAttribute('y', midY - 12);
                texto.setAttribute('class', 'peso-ruta');
                texto.setAttribute('text-anchor', 'middle');
                texto.setAttribute('fill', '#531e1e');
                texto.textContent = peso;

                rutasGroup.appendChild(texto);
            }
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

        // ✅ DEBUG: Verificar criterio
        console.log("🔍 DEBUG - Criterio actual:", this.criterioActual);

        this.actualizarEstado("Calculando ruta óptima...");
        this.limpiarAnimaciones();

        try {
            const response = await fetch('/api/ruta', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    origen, 
                    destino, 
                    criterio: this.criterioActual // ← AQUÍ ESTÁ EL PROBLEMA
                })
            });

            if (!response.ok) {
                throw new Error(`Error del servidor: ${response.status}`);
            }

            const data = await response.json();
            
            // ✅ DEBUG: Verificar respuesta
            console.log("🔍 DEBUG - Respuesta del servidor:", data);
            
            if (data.error) {
                document.getElementById('resultado').innerHTML = 
                    `<strong>❌ Error:</strong> ${data.error}`;
                this.actualizarEstado("Error en cálculo de ruta");
            } else {
                await this.animarDijkstra(data.pasos);
                this.dibujarRutaOptima(data.camino);
                this.mostrarResultado(data);
                this.actualizarEstado("Ruta calculada correctamente");
            }
                
        } catch (error) {
            document.getElementById('resultado').innerHTML = 
                `<strong>❌ Error:</strong> ${error.message}`;
            this.actualizarEstado("Error de conexión");
        }
    }


    mostrarResultado(data) {
        console.log("Datos recibidos:", data);
        const resultadoDiv = document.getElementById('resultado');
        
        const criterio = data.criterio === 'distancia' ? 'Distancia' : 'Tiempo';
        const unidad = data.criterio === 'distancia' ? 'km' : 'horas';
        
        resultadoDiv.innerHTML = `
            <h3>Ruta ${criterio.toLowerCase()} más corta</h3>
            <p><strong>Ruta:</strong> ${data.camino.join(' → ')}</p>
            <p><strong>${criterio} total:</strong> ${data.distancia} ${unidad}</p>
        `;
    }

    async animarDijkstra(pasos) {
        this.actualizarEstado("Animando algoritmo Dijkstra...");
        
        for (let i = 0; i < pasos.length; i++) {
            const [accion, ciudad, valor] = pasos[i];
            
            await new Promise(resolve => setTimeout(resolve, 300));
            
            const circulo = document.getElementById(`circulo-${ciudad}`);
            if (circulo) {
                if (accion === 'visitando') {
                    circulo.style.fill = '#ffd700';
                    circulo.style.stroke = '#ff6b00';
                } else if (accion === 'actualizando') {
                    circulo.style.fill = '#90ee90';
                    circulo.style.stroke = '#28a745';
                }
            }
        }
        
        setTimeout(() => {
            this.limpiarAnimaciones();
        }, 10);
    }

    limpiarAnimaciones() {
        Object.keys(this.ciudades).forEach(ciudad => {
            const circulo = document.getElementById(`circulo-${ciudad}`);
            if (circulo) {
                circulo.style.fill = '#4745b1ff';
                circulo.style.stroke = '#f2f700';
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

    async agregarCiudad() {
        const nombre = document.getElementById('nombre-ciudad').value.trim();
        const x = document.getElementById('x-ciudad').value;
        const y = document.getElementById('y-ciudad').value;

        if (!nombre || !x || !y) {
            alert('Por favor completa todos los campos');
            return;
        }

        this.actualizarEstado("Agregando ciudad...");

        try {
            const response = await fetch('/api/ciudad', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nombre, x, y })
            });

            const resultado = await response.json();

            if (resultado.status === 'ok') {
                document.getElementById('form-ciudad').reset();
                await this.cargarMapa();
                this.actualizarEstado("Ciudad agregada correctamente");
            } else {
                alert('Error: ' + resultado.message);
                this.actualizarEstado("Error agregando ciudad");
            }

        } catch (error) {
            alert('Error de conexión: ' + error.message);
            this.actualizarEstado("Error de conexión");
        }
    }

    async eliminarCiudad(nombre) {
        if (!confirm(`¿Estás seguro de eliminar la ciudad "${nombre}" y todas sus rutas?`)) {
            return;
        }

        this.actualizarEstado("Eliminando ciudad...");

        try {
            const response = await fetch('/api/ciudad', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nombre })
            });

            const resultado = await response.json();

            if (resultado.status === 'ok') {
                await this.cargarMapa();
                this.actualizarEstado("Ciudad eliminada correctamente");
            } else {
                alert('Error: ' + resultado.message);
                this.actualizarEstado("Error eliminando ciudad");
            }

        } catch (error) {
            alert('Error de conexión: ' + error.message);
            this.actualizarEstado("Error de conexión");
        }
    }



    async agregarRuta() {
        // ✅ OBTENER VALORES DEL FORMULARIO
        const ciudad1 = document.getElementById('ciudad1-ruta').value;
        const ciudad2 = document.getElementById('ciudad2-ruta').value;
        const distancia = document.getElementById('distancia-ruta').value;
        const tiempo = document.getElementById('tiempo-ruta').value;

        // ✅ VERIFICAR QUE TODOS LOS CAMPOS ESTÁN LLENOS
        if (!ciudad1 || !ciudad2 || !distancia || !tiempo) {
            alert('Por favor completa todos los campos: ciudad origen, ciudad destino, distancia y tiempo');
            return;
        }

        if (ciudad1 === ciudad2) {
            alert('Las ciudades deben ser diferentes');
            return;
        }

        this.actualizarEstado("Agregando ruta...");

        try {
            // ✅ PREPARAR DATOS PARA ENVIAR
            const datos = {
                ciudad1: ciudad1,
                ciudad2: ciudad2,
                distancia: parseFloat(distancia),
                tiempo: parseFloat(tiempo)
            };

            // ✅ ENVIAR AL ENDPOINT CORRECTO
            const response = await fetch('/api/ruta/nueva', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(datos)
            });

            const resultado = await response.json();

            if (resultado.status === 'ok') {
                // ✅ LIMPIAR FORMULARIO Y ACTUALIZAR MAPA
                document.getElementById('form-ruta').reset();
                await this.cargarMapa();
                this.actualizarEstado("Ruta agregada correctamente");
            } else {
                alert('Error: ' + resultado.message);
                this.actualizarEstado("Error agregando ruta");
            }

        } catch (error) {
            alert('Error de conexión: ' + error.message);
            this.actualizarEstado("Error de conexión");
        }
    }



    mostrarListaRutas() {
        const lista = document.getElementById('lista-rutas');
        lista.innerHTML = '';
        
        const rutasOrdenadas = [...this.conexiones].sort(([ciudad1A, ciudad2A], [ciudad1B, ciudad2B]) => {
            const rutaA = `${ciudad1A} ↔ ${ciudad2A}`;
            const rutaB = `${ciudad1B} ↔ ${ciudad2B}`;
            return rutaA.localeCompare(rutaB);
        });
        
        rutasOrdenadas.forEach(([ciudad1, ciudad2]) => {
            let peso = "?";
            const clave = `${ciudad1}-${ciudad2}`;
            const claveInversa = `${ciudad2}-${ciudad1}`;
            
            // ✅ USAR CRITERIO ACTUAL PARA MOSTRAR PESOS
            if (this.pesos[clave] !== undefined || this.pesos[claveInversa] !== undefined) {
                const datosPeso = this.pesos[clave] || this.pesos[claveInversa];
                
                if (typeof datosPeso === 'object') {
                    peso = datosPeso[this.criterioActual] || datosPeso['distancia'];
                } else {
                    peso = datosPeso;
                }
            }
            
            const unidad = this.criterioActual === 'distancia' ? 'km' : 'horas';
            
            const div = document.createElement('div');
            div.className = 'ruta-item';
            div.innerHTML = `
                <span>${ciudad1} ↔ ${ciudad2} (${peso} ${unidad})</span>
                <button onclick="window.sistemaRutas.eliminarRuta('${ciudad1}', '${ciudad2}')" 
                        class="btn-eliminar">🗑️</button>
            `;
            div.style.display = 'flex';
            div.style.justifyContent = 'space-between';
            div.style.alignItems = 'center';
            div.style.padding = '5px 0';
            div.style.borderBottom = '1px solid #eee';
            lista.appendChild(div);
        });
    }



    async eliminarRuta(ciudad1, ciudad2) {
        if (!confirm(`¿Estás seguro de eliminar la ruta entre ${ciudad1} y ${ciudad2}?`)) {
            return;
        }

        this.actualizarEstado("Eliminando ruta...");

        try {
            const response = await fetch('/api/ruta', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ciudad1, ciudad2 })
            });

            const resultado = await response.json();

            if (resultado.status === 'ok') {
                await this.cargarMapa();
                this.actualizarEstado("Ruta eliminada correctamente");
            } else {
                alert('Error: ' + resultado.message);
                this.actualizarEstado("Error eliminando ruta");
            }

        } catch (error) {
            alert('Error de conexión: ' + error.message);
            this.actualizarEstado("Error de conexión");
        }
    }

    configurarClicksMapa() {
        const mapa = document.getElementById('mapa');
        if (mapa) {
            mapa.addEventListener('click', (event) => {
                this.manejarClickMapa(event);
            });
            mapa.style.cursor = 'crosshair';
        }
    }

    manejarClickMapa(event) {
        const svg = document.getElementById('mapa');
        const point = svg.createSVGPoint();
        
        point.x = event.clientX;
        point.y = event.clientY;
        const svgPoint = point.matrixTransform(svg.getScreenCTM().inverse());
        
        const x = Math.round(svgPoint.x);
        const y = Math.round(svgPoint.y);
        
        const nombre = prompt(`📍 Agregar nueva ciudad en coordenadas (${x}, ${y})\n\nIngresa el nombre de la ciudad:`);
        
        if (nombre && nombre.trim()) {
            this.agregarCiudadDesdeClick(nombre.trim(), x, y);
        }
    }

    async agregarCiudadDesdeClick(nombre, x, y) {
        this.actualizarEstado("Agregando ciudad...");

        try {
            const response = await fetch('/api/ciudad', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nombre, x, y })
            });

            const resultado = await response.json();

            if (resultado.status === 'ok') {
                await this.cargarMapa();
                this.actualizarEstado(`Ciudad "${nombre}" agregada correctamente`);
            } else {
                alert('Error: ' + resultado.message);
                this.actualizarEstado("Error agregando ciudad");
            }

        } catch (error) {
            alert('Error de conexión: ' + error.message);
            this.actualizarEstado("Error de conexión");
        }
    }
    
    async exportarMapa() {
        const svg = document.getElementById('mapa');
        const clone = svg.cloneNode(true);
        
        const fondo = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        fondo.setAttribute('x', '0');
        fondo.setAttribute('y', '0');
        fondo.setAttribute('width', '1200');
        fondo.setAttribute('height', '1000');
        fondo.setAttribute('fill', '#bad6db');
        fondo.setAttribute('rx', '8');
        clone.insertBefore(fondo, clone.firstChild);

        const elementos = clone.querySelectorAll('*');
        elementos.forEach(elemento => {
            elemento.style.display = 'block';
            elemento.style.visibility = 'visible';
            elemento.style.opacity = '1';
        });

        const circulos = clone.querySelectorAll('.circulo-ciudad');
        circulos.forEach(circulo => {
            if (!circulo.getAttribute('fill') || circulo.getAttribute('fill').includes('rgb')) {
                circulo.setAttribute('fill', '#4745b1');
            }
            if (!circulo.getAttribute('stroke') || circulo.getAttribute('stroke').includes('rgb')) {
                circulo.setAttribute('stroke', '#260829');
            }
            circulo.setAttribute('stroke-width', '3');
        });

        const textos = clone.querySelectorAll('.nombre-ciudad, .peso-ruta');
        textos.forEach(texto => {
            if (!texto.getAttribute('fill') || texto.getAttribute('fill').includes('rgb')) {
                if (texto.classList.contains('nombre-ciudad')) {
                    texto.setAttribute('fill', '#0c330e');
                } else if (texto.classList.contains('peso-ruta')) {
                    texto.setAttribute('fill', '#531e1e');
                }
            }
        });

        const rutas = clone.querySelectorAll('.ruta');
        rutas.forEach(ruta => {
            if (!ruta.getAttribute('stroke')) {
                ruta.setAttribute('stroke', '#6cb3af');
            }
            ruta.setAttribute('stroke-width', '3');
            ruta.setAttribute('opacity', '0.8');
        });

        const rutasOptimas = clone.querySelectorAll('.ruta-optima');
        rutasOptimas.forEach(ruta => {
            if (!ruta.getAttribute('stroke')) {
                ruta.setAttribute('stroke', '#e70f0f');
            }
            ruta.setAttribute('stroke-width', '5');
            ruta.setAttribute('opacity', '0.9');
        });

        const svgData = new XMLSerializer().serializeToString(clone);
        const blob = new Blob([svgData], {type: 'image/svg+xml'});
        const url = URL.createObjectURL(blob);
        
        const downloadLink = document.createElement('a');
        downloadLink.href = url;
        downloadLink.download = `mapa_bolivia_${new Date().toISOString().split('T')[0]}.svg`;
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
        URL.revokeObjectURL(url);
        
        this.actualizarEstado("Mapa exportado como SVG");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.sistemaRutas = new SistemaRutas();
});

function calcularRuta() {
    window.sistemaRutas.calcularRuta();
}

function limpiarRuta() {
    window.sistemaRutas.limpiarRuta();
}

function exportarMapa() {
    window.sistemaRutas.exportarMapa();
}

function cerrarAplicacion() {
    if (confirm('¿Estás seguro de que quieres cerrar la aplicación?')) {
        window.close();
    }
}