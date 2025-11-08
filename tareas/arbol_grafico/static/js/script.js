/*
static/js/script.js
Controlador frontend para visualización de árbol binario
*/

// Configuración global
const CONFIG = {
    nodeRadius: 25,
    horizontalSpacing: 75,
    verticalSpacing: 75
};

// Estado de la aplicación
let estado = {
    arbolData: null,
    animacionActiva: false,
    mapaNodosNivel: new Map() // <-- CAMBIO 1: Nuevo mapa para búsqueda O(1)
};

// Estado para controlar modo de coloreado
let modoSimetria = false;
let infoNiveles = [];

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    cargarEstadisticas();
    setInterval(cargarEstadisticas, 3000);
});

// Funciones de utilidad
function mostrarMensaje(mensaje, tipo = 'info') {
    const mensajesDiv = document.getElementById('mensajes');
    mensajesDiv.innerHTML = `<div class="mensaje ${tipo}">${mensaje}</div>`;
    
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
    
    if (!valor || !/^-?\d+$/.test(valor)) {
        mostrarMensaje('Ingrese un valor numérico válido', 'error');
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
    }
}

async function insertarSerie() {
    if (estado.animacionActiva) return;
    
    const input = document.getElementById('nodoSerie');
    const serie = input.value.trim();
    
    if (!serie) {
        mostrarMensaje('Ingrese una serie de números', 'error');
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
    }
}

async function eliminarNodo() {
    if (estado.animacionActiva) return;
    
    const input = document.getElementById('eliminarNodo');
    const valor = input.value.trim();
    
    if (!valor || !/^-?\d+$/.test(valor)) {
        mostrarMensaje('Ingrese un valor numérico válido', 'error');
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
    }
}

async function buscarNodo() {
    const input = document.getElementById('buscarNodo');
    const valor = input.value.trim();
    
    if (!valor || !/^-?\d+$/.test(valor)) {
        mostrarMensaje('Ingrese un valor numérico válido', 'error');
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
    }
}


async function realizarRecorrido(tipo) {
    try {
        // 1. Obtener y mostrar lista en panel de resultados (como antes)
        const data = await fetchAPI(`/recorrido/${tipo}`);
        document.getElementById('resultados').innerHTML = 
            `<strong>Recorrido ${tipo}:</strong><br>${data.recorrido.join(' → ')}`;
        
        // 2. Ejecutar animación en paralelo
        animarRecorrido(tipo);
        
        // 3. Mensaje combinado
        mostrarMensaje(`📊 Mostrando y animando recorrido ${tipo}`, 'success');
        
    } catch (error) {
        mostrarMensaje('Error al realizar recorrido', 'error');
    }
}



async function limpiarArbol() {
    try {
        const data = await fetchAPI('/limpiar', { method: 'POST' });
        mostrarMensaje(data.mensaje, 'success');
        
        modoSimetria = false;
        infoNiveles = [];
        
        await actualizarVisualizacion();
        await cargarEstadisticas();
    } catch (error) {
        mostrarMensaje('Error al limpiar árbol', 'error');
    }
}

async function mostrarArbol2() {
    try {
        // Reset visual completo
        modoSimetria = false;
        infoNiveles = [];
        estado.mapaNodosNivel.clear();
        
        // Forzar actualización visual
        await actualizarVisualizacion();
        
        // Mostrar confirmación
        mostrarMensaje('✅ Vista del árbol restablecida a modo normal', 'success');
        
    } catch (error) {
        mostrarMensaje('Error al mostrar árbol: ' + error.message, 'error');
    }
}


async function mostrarArbol() {
    try {
        // Reset visual completo
        modoSimetria = false;
        infoNiveles = [];
        estado.mapaNodosNivel.clear();
        
        // Forzar actualización visual
        await actualizarVisualizacion();
        
        // 1. Mensaje en panel de Resultados (derecho)
        document.getElementById('resultados').innerHTML = 
            '<strong>🌳 Vista Normal Activada</strong><br>Árbol mostrado con colores estándar';
        
        // 2. Mensaje en panel de Mensajes (central)  
        mostrarMensaje('✅ Vista del árbol restablecida a modo normal', 'success');
        
    } catch (error) {
        mostrarMensaje('Error al mostrar árbol: ' + error.message, 'error');
    }
}





async function generarAleatorio() {
    const N = 8;
    const valores = Array.from({ length: N }, () => 
        Math.floor(Math.random() * 200) + 1
    );
    
    document.getElementById('nodoSerie').value = valores.join(' ');
    await insertarSerie();
}

// Funciones de simetría
async function verSimetriaNiveles() {
    try {
        const data = await fetchAPI('/simetria-niveles');
        infoNiveles = data.niveles_simetria;
        modoSimetria = true;
        
        await actualizarVisualizacion();
        mostrarResumenSimetriaNiveles(infoNiveles);
        mostrarMensaje('Análisis de simetría por niveles completado', 'success');
        
    } catch (error) {
        mostrarMensaje('Error al analizar simetría por niveles: ' + error.message, 'error');
    }
}

async function verificarSimetria() {
    try {
        const data = await fetchAPI('/simetrico');
        
        const resultadosDiv = document.getElementById('resultados');
        if (data.es_simetrico) {
            resultadosDiv.innerHTML = `
                <strong>✅ Árbol Simétrico</strong><br>
                <p>El árbol es estructuralmente simétrico (espejo).</p>
            `;
            mostrarMensaje('✅ ' + data.mensaje, 'success');
        } else {
            resultadosDiv.innerHTML = `
                <strong>❌ Árbol No Simétrico</strong><br>
                <p>El árbol NO es estructuralmente simétrico.</p>
            `;
            mostrarMensaje('❌ ' + data.mensaje, 'error');
        }
    } catch (error) {
        mostrarMensaje('Error al verificar simetría: ' + error.message, 'error');
    }
}

function mostrarResumenSimetriaNiveles(niveles) {
    const resultadosDiv = document.getElementById('resultados');
    let html = '<strong>📊 Análisis de Simetría por Niveles</strong><br>';
    
    niveles.forEach(nivel => {
        const color = nivel.simetrico ? '🟢' : '🔴';
        const estado = nivel.simetrico ? 'SIMÉTRICO' : 'ASIMÉTRICO';
        const nodosStr = nivel.nodos.map(n => n !== null ? `●${n}` : '∅').join(' ');
        
        html += `<div style="margin: 5px 0; color: ${nivel.simetrico ? 'green' : 'red'}">
            <strong>Nivel ${nivel.nivel}:</strong> ${nodosStr} ${color} ${estado}
        </div>`;
    });
    
    resultadosDiv.innerHTML = html;
}

// Funciones de visualización

async function actualizarVisualizacion() {
    try {
        // 1. VERIFICAR SI EL MODO SIMETRÍA ESTÁ ACTIVO
        if (modoSimetria) {
            const dataSimetria = await fetchAPI('/simetria-niveles');
            infoNiveles = dataSimetria.niveles_simetria;
            
            // 🚨 OPTIMIZACIÓN CLAVE: Crear el mapa de búsqueda
            estado.mapaNodosNivel = crearMapaNodosNivel(infoNiveles);
            
            mostrarResumenSimetriaNiveles(infoNiveles);
        } else {
            // Si el modo simetría se desactiva, limpiamos el mapa
            estado.mapaNodosNivel.clear(); 
        }

        // 2. OBTENER Y DIBUJAR LA ESTRUCTURA (como antes)
        const data = await fetchAPI('/estructura');
        estado.arbolData = data;
        dibujarArbol(data.raiz);
        
    } catch (error) {
        console.error('Error al actualizar visualización:', error);
        // Si algo falla, reseteamos el modo y el mapa
        modoSimetria = false;
        infoNiveles = [];
        estado.mapaNodosNivel.clear();
    }
}




function dibujarArbol(raiz) {
    const svg = document.getElementById('arbol-svg');
    svg.innerHTML = '';
    
    if (!raiz) {
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
    
    const svgRect = svg.getBoundingClientRect();
    const svgWidth = svgRect.width || 800;
    
    const posiciones = {};
    calcularPosicionesSimple(raiz, posiciones, 0, svgWidth / 2, svgWidth / 4);
    
    dibujarLineas(svg, raiz, posiciones);
    
    Object.keys(posiciones).forEach(valor => {
        const { x, y } = posiciones[valor];
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
    
    let colorNodo = '#667eea'; 
    const valorNumerico = parseInt(valor); // Valor del nodo como número

    // 🚨 BÚSQUEDA O(1): Usamos el mapa para encontrar la información de nivel al instante.
    if (modoSimetria && estado.mapaNodosNivel.size > 0) {
        
        // Busca el objeto nivelInfo directamente usando el valor del nodo como clave
        const nivelInfoCoincidente = estado.mapaNodosNivel.get(valorNumerico); 

        // Aplicar el color de Simetría si se encontró el nodo en el mapa
        if (nivelInfoCoincidente) {
            colorNodo = nivelInfoCoincidente.simetrico ? '#4CAF50' : '#F44336'; // Verde o Rojo
        }
    }
    
    // -------------------------------------------------------------
    // Resto del código de dibujo (Asegura la prioridad de estilo)
    // -------------------------------------------------------------
    
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', x);
    circle.setAttribute('cy', y);
    circle.setAttribute('r', CONFIG.nodeRadius);
    
    // Aplicación de color con alta prioridad (solución final al fallo de color)
    circle.setAttribute('fill', colorNodo); 
    circle.style.fill = colorNodo; 
    
    circle.setAttribute('stroke', '#5a6fd8');
    circle.setAttribute('stroke-width', '2');
    circle.setAttribute('class', 'nodo');
    circle.setAttribute('data-valor', valor);
    
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
    const nodos = document.querySelectorAll('[data-valor]');
    
    let encontrado = false;
    nodos.forEach(nodo => {
        const valorNodo = nodo.getAttribute('data-valor');
        
        if (parseInt(valorNodo) === parseInt(valor)) {
            nodo.style.fill = '#4CAF50';
            encontrado = true;
            
            setTimeout(() => {
                nodo.style.fill = '#667eea';
            }, 2000);
        }
    });
}

async function eliminarRama() {
    const input = document.getElementById('eliminarRama');
    const valor = input.value.trim();
    
    if (!valor || !/^-?\d+$/.test(valor)) {
        mostrarMensaje('Ingrese un valor numérico válido', 'error');
        return;
    }
    
    const valorInt = parseInt(valor);
    
    try {
        const dataBusqueda = await fetchAPI('/buscar', {
            method: 'POST',
            body: JSON.stringify({ valor: valorInt })
        });
        
        if (!dataBusqueda.encontrado) {
            mostrarMensaje(`El nodo ${valor} no existe en el árbol`, 'error');
            return;
        }
        
        const data = await fetchAPI('/eliminar-rama', {
            method: 'POST',
            body: JSON.stringify({ valor: valorInt })
        });
        
        input.value = '';
        
        if (data.exito) {
            mostrarMensaje(data.mensaje, 'success');
            document.getElementById('resultados').innerHTML = 
                `<strong>✅ Rama eliminada exitosamente</strong><br>
                 <strong>Nodos eliminados:</strong> ${data.rama_eliminada.join(' → ')}<br>
                 <strong>Total de nodos eliminados:</strong> ${data.cantidad_nodos}`;
            
            await actualizarVisualizacion();
            await cargarEstadisticas();
        } else {
            mostrarMensaje(data.mensaje, 'error');
            document.getElementById('resultados').innerHTML = 
                `<strong>❌ Error al eliminar rama</strong><br>${data.mensaje}`;
        }
        
    } catch (error) {
        mostrarMensaje('Error al eliminar rama: ' + error.message, 'error');
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
        const statsDiv = document.getElementById('estadisticas');
        statsDiv.innerHTML = '<p>Estadísticas no disponibles temporalmente</p>';
    }
}



async function verificarBalanceo() {
    try {
        const data = await fetchAPI('/verificar-balanceo');
        
        const resultadosDiv = document.getElementById('resultados');
        if (data.balanceado) {
            resultadosDiv.innerHTML = `
                <strong>✅ Árbol Balanceado</strong><br>
                <p>${data.mensaje}</p>
            `;
            mostrarMensaje('✅ ' + data.mensaje, 'success');
        } else {
            resultadosDiv.innerHTML = `
                <strong>⚠️ Árbol Desbalanceado</strong><br>
                <p>${data.mensaje}. Usa el botón "Balancear Árbol" para corregir.</p>
            `;
            mostrarMensaje('⚠️ ' + data.mensaje, 'warning');
        }
    } catch (error) {
        mostrarMensaje('Error al verificar balanceo: ' + error.message, 'error');
    }
}

async function balancearArbol() {
    if (estado.animacionActiva) return;
    
    try {
        estado.animacionActiva = true;
        
        // Ejecutamos la llamada POST para forzar el balanceo
        const data = await fetchAPI('/balancear', { method: 'POST' });
        
        mostrarMensaje(data.mensaje, data.exito ? 'success' : 'error');
        
        if (data.exito) {
            // Actualizar la visualización y estadísticas para mostrar el nuevo árbol
            await actualizarVisualizacion();
            await cargarEstadisticas();
            document.getElementById('resultados').innerHTML = `
                <strong>🌳 Balanceo Completo</strong><br>
                <p>El árbol ha sido reconstruido a su versión de altura mínima.</p>
            `;
        }
    } catch (error) {
        mostrarMensaje('Error al balancear árbol: ' + error.message, 'error');
    } finally {
        estado.animacionActiva = false;
    }
}



// --- NUEVA FUNCIÓN DE UTILIDAD: Crea un mapa de búsqueda O(1) ---
function crearMapaNodosNivel(infoNiveles) {
    const mapa = new Map();
    if (!infoNiveles) return mapa;

    for (const nivelInfo of infoNiveles) {
        for (const nodoValor of nivelInfo.nodos) {
            // Solo almacenamos nodos que existen (no 'null')
            if (nodoValor !== null) {
                // Clave: El valor del nodo (Number); Valor: El objeto nivelInfo
                mapa.set(Number(nodoValor), nivelInfo); 
            }
        }
    }
    return mapa;
}
// -----------------------------------------------------------------




function salir() {
    window.close();
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

/*
async function animarRecorrido(tipo) {
    try {
        const data = await fetchAPI(`/recorrido-animado/${tipo}`);
        const nodos = data.recorrido;
        
        // Desactivar modo simetría durante animación
        const simetriaAnterior = modoSimetria;
        modoSimetria = false;
        
        mostrarMensaje(`🎬 Animando recorrido ${tipo}...`, 'info');
        
        // Animación secuencial
        for (let i = 0; i < nodos.length; i++) {
            await new Promise(resolve => setTimeout(resolve, 800)); // Delay
            resaltarNodoAnimado(nodos[i], i + 1);
        }
        
        // Restaurar modo simetría si estaba activo
        modoSimetria = simetriaAnterior;
        await actualizarVisualizacion();
        
    } catch (error) {
        mostrarMensaje('Error en animación: ' + error.message, 'error');
    }
}

*/
async function animarRecorrido(tipo) {
    try {
        const data = await fetchAPI(`/recorrido-animado/${tipo}`);
        const nodos = data.recorrido;
        
        // Resetear colores anteriores
        resetearColoresAnimacion();
        
        mostrarMensaje(`🎬 Animando recorrido ${tipo}...`, 'info');
        
        // Array para trackear nodos visitados
        const nodosVisitados = new Set();
        
        for (let i = 0; i < nodos.length; i++) {
            await new Promise(resolve => setTimeout(resolve, 800));
            
            // Agregar nodo actual a visitados
            nodosVisitados.add(nodos[i]);
            
            // Aplicar colores: visitados=verde, actual=naranja
            aplicarColoresRecorrido(nodosVisitados, nodos[i]);
        }
        
        mostrarMensaje(`✅ Recorrido ${tipo} completado. Nodos verdes = visitados`, 'success');
        
    } catch (error) {
        mostrarMensaje('Error en animación: ' + error.message, 'error');
    }
}

function aplicarColoresRecorrido(nodosVisitados, nodoActual) {
    const elementos = document.querySelectorAll('[data-valor]');
    
    elementos.forEach(nodo => {
        const valor = parseInt(nodo.getAttribute('data-valor'));
        
        if (valor === nodoActual) {
            // Nodo actual - Naranja
            nodo.style.fill = '#FFA500';
            nodo.style.stroke = '#FF8C00';
        } else if (nodosVisitados.has(valor)) {
            // Nodo visitado - Verde
            nodo.style.fill = '#4CAF50';
            nodo.style.stroke = '#45a049';
        }
        // Los no visitados mantienen colores normales
    });
}

function resetearColoresAnimacion() {
    const elementos = document.querySelectorAll('[data-valor]');
    elementos.forEach(nodo => {
        nodo.style.fill = '';
        nodo.style.stroke = '';
    });
}





function resaltarNodoAnimado(valor, orden) {
    const nodos = document.querySelectorAll('[data-valor]');
    
    nodos.forEach(nodo => {
        const valorNodo = nodo.getAttribute('data-valor');
        if (parseInt(valorNodo) === valor) {
            // Resaltar temporalmente en color de animación
            nodo.style.fill = '#FFA500'; // Naranja para animación
            nodo.style.stroke = '#FF8C00';
            
            // Restaurar después de un tiempo
            setTimeout(() => {
                if (modoSimetria) {
                    // Si hay simetría, mantener esos colores
                    actualizarVisualizacion();
                } else {
                    // Volver al color normal
                    nodo.style.fill = '#667eea';
                    nodo.style.stroke = '#5a6fd8';
                }
            }, 600);
        }
    });
}