class VisualizadorArbolMvias {
    constructor() {
        this.svg = document.getElementById('arbolSVG');
        this.actualizarEstadisticas();
    }

    limpiarSVG() {
        while (this.svg.firstChild) {
            this.svg.removeChild(this.svg.firstChild);
        }
    }

    dibujarArbol(arbolData) {
        this.limpiarSVG();
        
        if (!arbolData) return;

        const anchoSVG = this.svg.clientWidth;
        const nivelHeight = 120;
        
        // Calcular dimensiones del árbol
        const dimensiones = this.calcularDimensiones(arbolData);
        
        // Calcular factor de escala para el ancho
        const anchoRequerido = dimensiones.ancho * 100;
        const escala = Math.min(1, anchoSVG / anchoRequerido);
        
        const startX = anchoSVG / 2;
        const startY = 80;

        this.dibujarNodo(arbolData, startX, startY, 0, anchoRequerido * escala / 2, nivelHeight, escala);
    }

    calcularDimensiones(nodo, nivel = 0) {
        if (!nodo) return { ancho: 0, altura: 0 };

        let anchoTotal = 100; // Ancho base por nodo
        let maxAltura = 1;

        // Calcular dimensiones de los hijos
        let anchoHijos = 0;
        let maxAlturaHijos = 0;
        
        for (let hijo of nodo.hijos) {
            if (hijo) {
                const dimHijo = this.calcularDimensiones(hijo, nivel + 1);
                anchoHijos += dimHijo.ancho;
                maxAlturaHijos = Math.max(maxAlturaHijos, dimHijo.altura);
            }
        }

        anchoTotal = Math.max(anchoTotal, anchoHijos);
        maxAltura += maxAlturaHijos;

        return { ancho: anchoTotal, altura: maxAltura };
    }

    dibujarNodo(nodo, x, y, nivel, espacio, nivelHeight, escala) {
        if (!nodo) return;

        // Dibujar líneas a los hijos primero (para que queden detrás)
        this.dibujarLineasAHijos(nodo, x, y, nivel, espacio, nivelHeight, escala);

        // Dibujar el nodo
        const radio = 30 + (nodo.valores.length * 5);
        const grupoNodo = document.createElementNS("http://www.w3.org/2000/svg", "g");
        
        // Círculo del nodo
        const circulo = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circulo.setAttribute("cx", x);
        circulo.setAttribute("cy", y);
        circulo.setAttribute("r", radio);
        circulo.classList.add("nodo");
        
        if (nodo.esta_lleno) {
            circulo.classList.add("nodo-lleno");
        } else if (nodo.cantidad_valores === 0) {
            circulo.classList.add("nodo-vacio");
        }
        
        grupoNodo.appendChild(circulo);

        // Texto con los valores
        const texto = document.createElementNS("http://www.w3.org/2000/svg", "text");
        texto.setAttribute("x", x);
        texto.setAttribute("y", y);
        texto.textContent = nodo.valores.join(", ");
        texto.classList.add("texto-nodo");
        grupoNodo.appendChild(texto);

        // Información del nodo (cantidad de hijos)
        const info = document.createElementNS("http://www.w3.org/2000/svg", "text");
        info.setAttribute("x", x);
        info.setAttribute("y", y + 15);
        info.textContent = `Hijos: ${nodo.cantidad_hijos}`;
        info.classList.add("info-nodo");
        grupoNodo.appendChild(info);

        this.svg.appendChild(grupoNodo);

        // Dibujar hijos
        const hijosNoNulos = nodo.hijos.filter(h => h !== null);
        if (hijosNoNulos.length > 0) {
            const espacioHijo = espacio / hijosNoNulos.length;
            let currentX = x - espacio / 2 + espacioHijo / 2;
            
            for (let i = 0; i < nodo.hijos.length; i++) {
                if (nodo.hijos[i]) {
                    this.dibujarNodo(
                        nodo.hijos[i],
                        currentX,
                        y + nivelHeight,
                        nivel + 1,
                        espacioHijo,
                        nivelHeight,
                        escala
                    );
                    currentX += espacioHijo;
                }
            }
        }
    }

    dibujarLineasAHijos(nodo, x, y, nivel, espacio, nivelHeight, escala) {
        const hijosNoNulos = nodo.hijos.filter(h => h !== null);
        if (hijosNoNulos.length === 0) return;

        const espacioHijo = espacio / hijosNoNulos.length;
        let currentX = x - espacio / 2 + espacioHijo / 2;
        
        for (let i = 0; i < nodo.hijos.length; i++) {
            if (nodo.hijos[i]) {
                const linea = document.createElementNS("http://www.w3.org/2000/svg", "line");
                linea.setAttribute("x1", x);
                linea.setAttribute("y1", y + 30);
                linea.setAttribute("x2", currentX);
                linea.setAttribute("y2", y + nivelHeight - 30);
                linea.classList.add("linea");
                this.svg.appendChild(linea);
                
                currentX += espacioHijo;
            }
        }
    }

    actualizarEstadisticas(estadisticas = null) {
        if (estadisticas) {
            document.getElementById('totalNodos').textContent = estadisticas.total_nodos;
            document.getElementById('utilizacionPromedio').textContent = 
                (estadisticas.utilizacion_promedio * 100).toFixed(1) + '%';
        } else {
            document.getElementById('totalNodos').textContent = '0';
            document.getElementById('utilizacionPromedio').textContent = '0%';
        }
    }

    mostrarResultado(mensaje, esExito = true) {
        const resultadosDiv = document.getElementById('resultados');
        resultadosDiv.innerHTML = `<div class="${esExito ? 'success' : 'error'}">${mensaje}</div>`;
        
        setTimeout(() => {
            resultadosDiv.innerHTML = '';
        }, 3000);
    }
}

// Función para dar feedback visual en el input
function mostrarFeedbackInput(esExito) {
    const input = document.getElementById('valorInput');
    input.classList.remove('input-error', 'input-success');
    
    if (esExito === true) {
        input.classList.add('input-success');
    } else if (esExito === false) {
        input.classList.add('input-error');
    }
    
    // Remover las clases después de 2 segundos
    setTimeout(() => {
        input.classList.remove('input-error', 'input-success');
    }, 2000);
}

// Instancia global del visualizador
const visualizador = new VisualizadorArbolMvias();

// Funciones de interfaz
async function insertar() {
    const valorInput = document.getElementById('valorInput');
    const valor = parseInt(valorInput.value);
    
    if (isNaN(valor)) {
        visualizador.mostrarResultado('Por favor ingrese un número válido', false);
        mostrarFeedbackInput(false);
        return;
    }

    try {
        const response = await fetch('/insertar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ valor: valor })
        });

        const data = await response.json();
        
        if (data.success) {
            visualizador.dibujarArbol(data.arbol);
            visualizador.actualizarEstadisticas(data.estadisticas);
            visualizador.mostrarResultado(`Valor ${valor} insertado correctamente`);
            valorInput.value = '';
            mostrarFeedbackInput(true);
            valorInput.focus();
        } else {
            visualizador.mostrarResultado(`Error: ${data.error}`, false);
            mostrarFeedbackInput(false);
            valorInput.focus();
            valorInput.select();
        }
    } catch (error) {
        visualizador.mostrarResultado('Error de conexión', false);
        mostrarFeedbackInput(false);
    }
}

async function buscar() {
    const valorInput = document.getElementById('valorInput');
    const valor = parseInt(valorInput.value);
    
    if (isNaN(valor)) {
        visualizador.mostrarResultado('Por favor ingrese un número válido', false);
        mostrarFeedbackInput(false);
        return;
    }

    try {
        const response = await fetch('/buscar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ valor: valor })
        });

        const data = await response.json();
        
        if (data.success) {
            visualizador.dibujarArbol(data.arbol);
            if (data.encontrado) {
                visualizador.mostrarResultado(`Valor ${valor} encontrado en el árbol`);
                mostrarFeedbackInput(true);
            } else {
                visualizador.mostrarResultado(`Valor ${valor} no encontrado en el árbol`, false);
                mostrarFeedbackInput(false);
            }
        } else {
            visualizador.mostrarResultado(`Error: ${data.error}`, false);
            mostrarFeedbackInput(false);
        }
    } catch (error) {
        visualizador.mostrarResultado('Error de conexión', false);
        mostrarFeedbackInput(false);
    }
}

async function realizarRecorrido() {
    const tipo = document.getElementById('recorridoSelect').value;
    
    try {
        const response = await fetch(`/recorrido/${tipo}`);
        const data = await response.json();
        
        if (data.success) {
            let nombreRecorrido = '';
            switch(data.tipo) {
                case 'inorden': nombreRecorrido = 'Inorden'; break;
                case 'preorden': nombreRecorrido = 'Preorden'; break;
                case 'niveles': nombreRecorrido = 'Por Niveles'; break;
            }
            
            visualizador.mostrarResultado(
                `${nombreRecorrido}: [${data.recorrido.join(', ')}]`
            );
        } else {
            visualizador.mostrarResultado(`Error: ${data.error}`, false);
        }
    } catch (error) {
        visualizador.mostrarResultado('Error de conexión', false);
    }
}

async function limpiarArbol() {
    try {
        const response = await fetch('/limpiar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const data = await response.json();
        
        if (data.success) {
            visualizador.limpiarSVG();
            visualizador.actualizarEstadisticas(data.estadisticas);
            visualizador.mostrarResultado('Árbol limpiado correctamente');
        } else {
            visualizador.mostrarResultado(`Error: ${data.error}`, false);
        }
    } catch (error) {
        visualizador.mostrarResultado('Error de conexión', false);
    }
}

// Cargar árbol al iniciar
document.addEventListener('DOMContentLoaded', async function() {
    try {
        const response = await fetch('/arbol');
        const data = await response.json();
        
        if (data.success) {
            visualizador.dibujarArbol(data.arbol);
            visualizador.actualizarEstadisticas(data.estadisticas);
        }
    } catch (error) {
        console.error('Error al cargar el árbol inicial:', error);
    }
});

// Permitir Enter en el input
document.getElementById('valorInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        insertar();
    }
});

// Limpiar feedback visual cuando el usuario empiece a escribir
document.getElementById('valorInput').addEventListener('input', function() {
    this.classList.remove('input-error', 'input-success');
});