 // Configuración global
const CONFIG = {
    nodeRadius: 25,
    horizontalSpacing: 75,
    verticalSpacing: 75,
    animationDuration: 500
};

// Estado de la aplicación
let estado = {
    arbolData: null,
    nodosSeleccionados: new Set(),
    animacionActiva: false
};

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    cargarEstadisticas();
    setInterval(cargarEstadisticas, 3000); // Actualizar estadísticas cada 3 segundos
});

// Funciones de utilidad
function mostrarMensaje(mensaje, tipo = 'info') {
    const mensajesDiv = document.getElementById('mensajes');
    mensajesDiv.innerHTML = `<div class="mensaje ${tipo}">${mensaje}</div>`;
    
    if (tipo === 'error') {
        console.error(mensaje);
    } else {
        console.log(mensaje);
    }
}

function limpiarMensajes() {
    setTimeout(() => {
        document.getElementById('mensajes').innerHTML = '';
    }, 3000);
}

// Funciones de comunicación con el backend
async function fetchAPI(endpoint, options = {}) {
    try {
        const response = await fetch(endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        mostrarMensaje(`Error de conexión: ${error.message}`, 'error');
        throw error;
    }
}

// Funciones principales de la interfaz
async function insertarIndividual() {
    if (estado.animacionActiva) return;
    
    const input = document.getElementById('nodoIndividual');
    const valor = input.value.trim();
    
    if (!valor) {
        mostrarMensaje('Ingrese un valor numérico', 'error');
        return;
    }
    
    if (!/^-?\d+$/.test(valor)) {
        mostrarMensaje('Solo se permiten números enteros', 'error');
        return;
    }
    
    try {
        estado.animacionActiva = true;
        const data = await fetchAPI('/insertar', {
            method: 'POST',
            body: JSON.stringify({ valores: [valor] })
        });
        
        input.value = '';
        mostrarMensaje(data.resultados[0].mensaje, data.resultados[0].exito ? 'success' : 'error');
        
        if (data.resultados[0].exito) {
            await actualizarVisualizacion();
            await cargarEstadisticas();
        }
        
    } catch (error) {
        mostrarMensaje('Error al insertar nodo', 'error');
    } finally {
        estado.animacionActiva = false;
        limpiarMensajes();
    }
}

async function insertarSerie() {
    if (estado.animacionActiva) return;
    
    const input = document.getElementById('nodoSerie');
    const serie = input.value.trim();
    
    if (!serie) {
        mostrarMensaje('Ingrese una serie de números separados por espacios', 'error');
        return;
    }
    
    const valores = serie.split(/\s+/).filter(v => v !== '');
    const valoresValidos = valores.filter(v => /^-?\d+$/.test(v));
    const valoresInvalidos = valores.filter(v => !/^-?\d+$/.test(v));
    
    if (valoresInvalidos.length > 0) {
        mostrarMensaje(`Valores inválidos ignorados: ${valoresInvalidos.join(', ')}`, 'error');
    }
    
    if (valoresValidos.length === 0) {
        mostrarMensaje('No hay valores válidos para insertar', 'error');
        return;
    }
    
    try {
        estado.animacionActiva = true;
        const data = await fetchAPI('/insertar', {
            method: 'POST',
            body: JSON.stringify({ valores: valoresValidos })
        });
        
        input.value = '';
        
        // Mostrar resumen de inserciones
        const exitosas = data.resultados.filter(r => r.exito).length;
        const duplicados = data.resultados.filter(r => !r.exito).length;
        
        mostrarMensaje(
            `Inserción completada: ${exitosas} exitosas, ${duplicados} duplicados ignorados`,
            'success'
        );
        
        await actualizarVisualizacion();
        await cargarEstadisticas();
        
    } catch (error) {
        mostrarMensaje('Error al insertar serie', 'error');
    } finally {
        estado.animacionActiva = false;
        limpiarMensajes();
    }
}

async function eliminarNodo() {
    if (estado.animacionActiva) return;
    
    const input = document.getElementById('eliminarNodo');
    const valor = input.value.trim();
    
    if (!valor) {
        mostrarMensaje('Ingrese un valor a eliminar', 'error');
        return;
    }
    
    if (!/^-?\d+$/.test(valor)) {
        mostrarMensaje('Solo se permiten números enteros', 'error');
        return;
    }
    
    try {
        estado.animacionActiva = true;
        const data = await fetchAPI('/eliminar', {
            method: 'POST',
            body: JSON.stringify({ valor: parseInt(valor) })
        });
        
        input.value = '';
        mostrarMensaje(data.mensaje, data.exito ? 'success' : 'error');
        
        if (data.exito) {
            await actualizarVisualizacion();
            await cargarEstadisticas();
        }
        
    } catch (error) {
        mostrarMensaje('Error al eliminar nodo', 'error');
    } finally {
        estado.animacionActiva = false;
        limpiarMensajes();
    }
}

async function buscarNodo() {
    const input = document.getElementById('buscarNodo');
    const valor = input.value.trim();
    
    if (!valor) {
        mostrarMensaje('Ingrese un valor a buscar', 'error');
        return;
    }
    
    if (!/^-?\d+$/.test(valor)) {
        mostrarMensaje('Solo se permiten números enteros', 'error');
        return;
    }
    
    try {
        const data = await fetchAPI('/buscar', {
            method: 'POST',
            body: JSON.stringify({ valor: parseInt(valor) })
        });
        
        input.value = '';
        mostrarMensaje(data.mensaje, data.encontrado ? 'success' : 'error');
        
        if (data.encontrado) {
            resaltarNodo(parseInt(valor));
        }
        
    } catch (error) {
        mostrarMensaje('Error al buscar nodo', 'error');
    } finally {
        limpiarMensajes();
    }
}

async function realizarRecorrido(tipo) {
    try {
        const data = await fetchAPI(`/recorrido/${tipo}`);
        document.getElementById('resultados').innerHTML = 
            `<strong>Recorrido ${tipo}:</strong><br>${data.recorrido.join(' → ')}`;
    } catch (error) {
        mostrarMensaje('Error al realizar recorrido', 'error');
    }
}

async function limpiarArbol() {

    /*
    if (!confirm('¿Está seguro de que desea limpiar el árbol completo?')) {
        return;
    }
    */
    try {
        const data = await fetchAPI('/limpiar', { method: 'POST' });
        mostrarMensaje(data.mensaje, 'success');
        await actualizarVisualizacion();
        await cargarEstadisticas();
    } catch (error) {
        mostrarMensaje('Error al limpiar árbol', 'error');
    }
}

async function generarAleatorio() {
    // Generar N números aleatorios entre 1 y 100
    N = 6
    const valores = Array.from({ length: N }, () => 
        Math.floor(Math.random() * 200) + 1
    );
    
    document.getElementById('nodoSerie').value = valores.join(' ');
    await insertarSerie();
}


async function actualizarVisualizacion() {
    try {
        console.log("🔄 Actualizando visualización...");
        const data = await fetchAPI('/estructura');
        console.log("📊 Datos recibidos:", data);
        estado.arbolData = data;
        dibujarArbol(data.raiz);
    } catch (error) {
        console.error('❌ Error al actualizar visualización:', error);
    }
}


function dibujarArbol(raiz) {
    console.log("🎨 Iniciando dibujo del árbol");
    const svg = document.getElementById('arbol-svg');
    svg.innerHTML = '';
    
    if (!raiz) {
        console.log("ℹ️ El árbol está vacío");
        // Dibujar mensaje en el centro del SVG
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', '50%');
        text.setAttribute('y', '50%');
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('fill', '#666');
        text.setAttribute('font-size', '16px');
        text.textContent = 'Árbol vacío - Inserta nodos para comenzar';
        svg.appendChild(text);
        return;
    }
    
    // Calcular dimensiones del SVG
    const svgRect = svg.getBoundingClientRect();
    const svgWidth = svgRect.width || 800;
    const svgHeight = svgRect.height || 600;
    
    console.log(`📐 Dimensiones SVG: ${svgWidth}x${svgHeight}`);
    
    // Calcular posiciones
    const posiciones = {};
    calcularPosicionesSimple(raiz, posiciones, 0, svgWidth / 2, svgWidth / 4);
    
    console.log("📍 Posiciones calculadas:", posiciones);
    
    // Dibujar líneas primero
    dibujarLineas(svg, raiz, posiciones);
    
    // Dibujar nodos
    Object.keys(posiciones).forEach(valor => {
        const { x, y } = posiciones[valor];
        console.log(`🔘 Dibujando nodo ${valor} en (${x}, ${y})`);
        dibujarNodo(svg, valor, x, y);
    });

    
}

function calcularPosicionesSimple(nodo, posiciones, nivel, x, offset) {
    if (!nodo) return;
    
    posiciones[nodo.dato] = { x, y: nivel * CONFIG.verticalSpacing + 50 };
    
    if (nodo.izquierdo) {
        calcularPosicionesSimple(nodo.izquierdo, posiciones, nivel + 1, x - offset, offset / 2);
    }
    if (nodo.derecho) {
        calcularPosicionesSimple(nodo.derecho, posiciones, nivel + 1, x + offset, offset / 2);
    }
}


function dibujarLineas(svg, nodo, posiciones) {
    if (!nodo) return;
    
    const currentPos = posiciones[nodo.dato];
    
    if (nodo.izquierdo) {
        const leftPos = posiciones[nodo.izquierdo.dato];
        dibujarLinea(svg, currentPos.x, currentPos.y, leftPos.x, leftPos.y);
        dibujarLineas(svg, nodo.izquierdo, posiciones);
    }
    
    if (nodo.derecho) {
        const rightPos = posiciones[nodo.derecho.dato];
        dibujarLinea(svg, currentPos.x, currentPos.y, rightPos.x, rightPos.y);
        dibujarLineas(svg, nodo.derecho, posiciones);
    }
}

function dibujarLinea(svg, x1, y1, x2, y2) {
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', x1);
    line.setAttribute('y1', y1);
    line.setAttribute('x2', x2);
    line.setAttribute('y2', y2);
    line.setAttribute('stroke', '#666');
    line.setAttribute('stroke-width', '2');
    svg.appendChild(line);
}

function dibujarNodo(svg, valor, x, y) {
    const grupo = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    
    // Círculo del nodo
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', x);
    circle.setAttribute('cy', y);
    circle.setAttribute('r', CONFIG.nodeRadius);
    circle.setAttribute('fill', '#667eea');
    circle.setAttribute('stroke', '#5a6fd8');
    circle.setAttribute('stroke-width', '2');
    circle.setAttribute('class', 'nodo');
    circle.setAttribute('data-valor', valor);
    
    // Texto del valor
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', x);
    text.setAttribute('y', y + 5);
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('fill', 'white');
    text.setAttribute('font-weight', 'bold');
    text.setAttribute('font-size', '20px');
    text.textContent = valor;
    
    grupo.appendChild(circle);
    grupo.appendChild(text);
    svg.appendChild(grupo);
}


function resaltarNodo(valor) {
    console.log("Buscando nodo con valor:", valor);
    
    // Buscar todos los elementos con data-valor
    const nodos = document.querySelectorAll('[data-valor]');
    console.log("Nodos encontrados en el SVG:", nodos.length);
    
    let encontrado = false;
    nodos.forEach(nodo => {
        const valorNodo = nodo.getAttribute('data-valor');
        console.log("Nodo valor:", valorNodo, "Buscando:", valor);
        
        if (parseInt(valorNodo) === parseInt(valor)) {
            console.log("¡Nodo encontrado! Resaltando...");
            nodo.style.fill = '#4CAF50';
            encontrado = true;
            
            // Quitar el resaltado después de 2 segundos
            setTimeout(() => {
                nodo.style.fill = '#667eea';
            }, 2000);
        }
    });
    
    if (!encontrado) {
        console.log("Nodo no encontrado en la visualización");
    }
}


async function cargarEstadisticas() {
    try {
        const data = await fetchAPI('/estadisticas');
        const statsDiv = document.getElementById('estadisticas');
        
        if (data.vacio) {
            statsDiv.innerHTML = '<p>El árbol está vacío</p>';
        } else {
            statsDiv.innerHTML = `
                <p><strong>Altura:</strong> ${data.altura}</p>
                <p><strong>Total nodos:</strong> ${data.total_nodos}</p>
                <p><strong>Nodos hoja:</strong> ${data.nodos_hoja}</p>
                <p><strong>Nodos internos:</strong> ${data.total_nodos - data.nodos_hoja}</p>
            `;
        }
    } catch (error) {        
        // En caso de error, mostramos un mensaje pero no fallamos
        console.error('Error al cargar estadísticas:', error);
        const statsDiv = document.getElementById('estadisticas');
        statsDiv.innerHTML = '<p>Estadísticas no disponibles temporalmente</p>';
    }
}

// Event listeners para teclado
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const activeElement = document.activeElement;
        if (activeElement.id === 'nodoIndividual') {
            insertarIndividual();
        } else if (activeElement.id === 'nodoSerie') {
            insertarSerie();
        } else if (activeElement.id === 'eliminarNodo') {
            eliminarNodo();
        } else if (activeElement.id === 'buscarNodo') {
            buscarNodo();
        }
    }
});

async function eliminarRama() {
    const input = document.getElementById('eliminarRama');
    const valor = input.value.trim();
    
    if (!valor) {
        mostrarMensaje('Ingrese un valor para eliminar la rama', 'error');
        return;
    }
    
    if (!/^-?\d+$/.test(valor)) {
        mostrarMensaje('Solo se permiten números enteros', 'error');
        return;
    }
    
    const valorInt = parseInt(valor);
    
    // Primero verificamos si el nodo existe
    try {
        const dataBusqueda = await fetchAPI('/buscar', {
            method: 'POST',
            body: JSON.stringify({ valor: valorInt })
        });
        
        if (!dataBusqueda.encontrado) {
            mostrarMensaje(`El nodo ${valor} no existe en el árbol`, 'error');
            return;
        }
        
        /*
        if (!confirm(`
            ¿Está seguro de que desea eliminar toda la rama que comienza
             en el nodo ${valor}? Esta acción eliminará el nodo ${valor} y 
            todos sus descendientes. Esta acción no se puede deshacer.`)) {
            return;
        }
        
        */
        const data = await fetchAPI('/eliminar-rama', {
            method: 'POST',
            body: JSON.stringify({ valor: valorInt })
        });
        
        input.value = '';
        
        if (data.exito) {
            mostrarMensaje(data.mensaje, 'success');
            // Mostrar información detallada de la rama eliminada
            document.getElementById('resultados').innerHTML = 
                `<strong>✅ Rama eliminada exitosamente</strong><br>
                 <strong>Nodos eliminados:</strong> ${data.rama_eliminada.join(' → ')}<br>
                 <strong>Total de nodos eliminados:</strong> ${data.cantidad_nodos}`;
            
            await actualizarVisualizacion();
            await cargarEstadisticas();
        } else {
            mostrarMensaje(data.mensaje, 'error');
            document.getElementById('resultados').innerHTML = 
                `<strong>❌ Error al eliminar rama</strong><br>
                 ${data.mensaje}`;
        }
        
    } catch (error) {
        mostrarMensaje('Error al eliminar rama: ' + error.message, 'error');
    }
}





async function mostrarInfoRama() {
    const valor = prompt('Ingrese el valor del nodo para ver información de su rama:');
    
    if (!valor || !/^-?\d+$/.test(valor)) {
        mostrarMensaje('Valor no válido', 'error');
        return;
    }
    
    try {
        // Usaremos el endpoint de búsqueda y luego calcularemos la rama
        const dataBusqueda = await fetchAPI('/buscar', {
            method: 'POST',
            body: JSON.stringify({ valor: parseInt(valor) })
        });
        
        if (!dataBusqueda.encontrado) {
            mostrarMensaje('Nodo no encontrado', 'error');
            return;
        }
        
        // Para obtener la rama, necesitamos un endpoint específico
        // Por ahora, mostramos un mensaje informativo
        mostrarMensaje(`Nodo ${valor} encontrado. Use "Eliminar Rama" para ver información detallada.`, 'info');
        
    } catch (error) {
        mostrarMensaje('Error al obtener información de la rama', 'error');
    }
}



async function verificarRama() {
    const valor = prompt('Ingrese el valor del nodo para ver información de su rama:');
    
    if (!valor || !/^-?\d+$/.test(valor)) {
        mostrarMensaje('Valor no válido', 'error');
        return;
    }
    
    try {
        const dataBusqueda = await fetchAPI('/buscar', {
            method: 'POST',
            body: JSON.stringify({ valor: parseInt(valor) })
        });
        
        if (!dataBusqueda.encontrado) {
            mostrarMensaje(`El nodo ${valor} no existe en el árbol`, 'error');
            return;
        }
        
        // Para obtener información detallada de la rama, necesitamos un endpoint
        // Por ahora, usamos uno temporal o mostramos información básica
        mostrarMensaje(`El nodo ${valor} existe. Puede eliminar toda su rama usando el botón "Eliminar Rama".`, 'info');
        
    } catch (error) {
        mostrarMensaje('Error al verificar la rama', 'error');
    }
}

function salir() {

    window.close();

}