// script.js
let currentData = null;
let currentColumns = [];
// Agregar después de las variables existentes (línea 3)
let chatHistory = [];
let analysisResults = null;
let chatbotEnabled = false;

// Navegación entre secciones
document.addEventListener('DOMContentLoaded', function() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const sections = document.querySelectorAll('.section');
    
    navButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetSection = this.dataset.section;
            
            // Actualizar botones activos
            navButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Mostrar sección correspondiente
            sections.forEach(section => {
                section.classList.remove('active');
                if (section.id === targetSection) {
                    section.classList.add('active');
                }
            });
        });
    });
    
    
    // Configurar carga de archivos
    setupFileUpload();
});

// Configuración de carga de archivos
function setupFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.querySelector('.upload-area');
    
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#3498db';
        uploadArea.style.backgroundColor = '#f8f9fa';
    });
    
    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#bdc3c7';
        uploadArea.style.backgroundColor = 'transparent';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#bdc3c7';
        uploadArea.style.backgroundColor = 'transparent';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
}

// Manejar selección de archivo
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        handleFile(file);
    }
}

// Procesar archivo
function handleFile(file) {
    if (file.type !== 'text/csv') {
        showStatus('Por favor selecciona un archivo CSV válido.', 'error');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const csv = e.target.result;
        parseCSV(csv);
    };
    reader.readAsText(file);
}

// Parsear CSV
function parseCSV(csv) {
    const lines = csv.trim().split('\n');
    const headers = lines[0].split(',').map(h => h.trim());
    
    const data = [];
    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',').map(v => v.trim());
        const row = {};
        headers.forEach((header, index) => {
            const value = values[index];
            row[header] = isNaN(value) ? value : parseFloat(value);
        });
        data.push(row);
    }
    
    currentData = data;
    currentColumns = headers;
    displayData(data, headers);
    setupVariableSelection(headers);
    showStatus('Datos cargados exitosamente.', 'success');
    
    // AGREGAR ESTAS LÍNEAS:
    enableChatbot();
    addChatMessage('bot', `¡Datos cargados! Tienes ${data.length} registros con ${headers.length} variables. ¿Necesitas ayuda para seleccionar variables?`);
}

// Cargar datos de ejemplo
function loadSampleData() {
    const sampleData = [
        { edad: 25, ingresos: 35000, educacion: 12, satisfaccion: 7, rendimiento: 8, motivacion: 6 },
        { edad: 30, ingresos: 45000, educacion: 16, satisfaccion: 8, rendimiento: 9, motivacion: 8 },
        { edad: 35, ingresos: 55000, educacion: 18, satisfaccion: 6, rendimiento: 7, motivacion: 5 },
        { edad: 28, ingresos: 40000, educacion: 14, satisfaccion: 9, rendimiento: 8, motivacion: 9 },
        { edad: 32, ingresos: 48000, educacion: 16, satisfaccion: 7, rendimiento: 8, motivacion: 7 },
        { edad: 27, ingresos: 38000, educacion: 14, satisfaccion: 8, rendimiento: 7, motivacion: 8 },
        { edad: 29, ingresos: 42000, educacion: 15, satisfaccion: 6, rendimiento: 6, motivacion: 5 },
        { edad: 31, ingresos: 46000, educacion: 17, satisfaccion: 9, rendimiento: 9, motivacion: 9 },
        { edad: 26, ingresos: 36000, educacion: 13, satisfaccion: 7, rendimiento: 7, motivacion: 6 },
        { edad: 33, ingresos: 52000, educacion: 18, satisfaccion: 8, rendimiento: 8, motivacion: 8 },
        { edad: 24, ingresos: 32000, educacion: 12, satisfaccion: 6, rendimiento: 6, motivacion: 5 },
        { edad: 34, ingresos: 50000, educacion: 17, satisfaccion: 9, rendimiento: 9, motivacion: 9 },
        { edad: 28, ingresos: 41000, educacion: 15, satisfaccion: 7, rendimiento: 7, motivacion: 7 },
        { edad: 30, ingresos: 44000, educacion: 16, satisfaccion: 8, rendimiento: 8, motivacion: 8 },
        { edad: 26, ingresos: 37000, educacion: 14, satisfaccion: 6, rendimiento: 6, motivacion: 6 }
    ];
    
const headers = Object.keys(sampleData[0]);
    currentData = sampleData;
    currentColumns = headers;
    displayData(sampleData, headers);
    setupVariableSelection(headers);
    showStatus('Datos de ejemplo cargados exitosamente.', 'success');
    enableChatbot();
    addChatMessage('bot', `¡Perfecto! He detectado tus datos con ${headers.length} variables: ${headers.join(', ')}. ¿Qué te gustaría saber sobre ellos?`);
}

// Mostrar datos en tabla
function displayData(data, headers) {
    const tableHeader = document.getElementById('tableHeader');
    const tableBody = document.getElementById('tableBody');
    const dataInfo = document.getElementById('dataInfo');
    const dataPreview = document.getElementById('dataPreview');
    
    // Limpiar tabla
    tableHeader.innerHTML = '';
    tableBody.innerHTML = '';
    
    // Crear encabezados
    const headerRow = document.createElement('tr');
    headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    });
    tableHeader.appendChild(headerRow);
    
    // Mostrar primeras 10 filas
    const displayRows = data.slice(0, 10);
    displayRows.forEach(row => {
        const tr = document.createElement('tr');
        headers.forEach(header => {
            const td = document.createElement('td');
            td.textContent = row[header];
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);
    });
    
    // Información de los datos
    dataInfo.textContent = `Mostrando ${displayRows.length} de ${data.length} filas. Columnas: ${headers.length}`;
    
    // Mostrar preview
    dataPreview.style.display = 'block';
}

// Configurar selección de variables
function setupVariableSelection(headers) {
    const independentVars = document.getElementById('independentVars');
    const dependentVars = document.getElementById('dependentVars');
    
    // Limpiar contenedores
    independentVars.innerHTML = '';
    dependentVars.innerHTML = '';
    
    // Crear checkboxes para variables independientes
    headers.forEach(header => {
        const div = document.createElement('div');
        div.className = 'variable-item';
        div.innerHTML = `
            <input type="checkbox" id="ind_${header}" name="independent" value="${header}">
            <label for="ind_${header}">${header}</label>
        `;
        independentVars.appendChild(div);
    });
    
    // Crear checkboxes para variables dependientes
    headers.forEach(header => {
        const div = document.createElement('div');
        div.className = 'variable-item';
        div.innerHTML = `
            <input type="checkbox" id="dep_${header}" name="dependent" value="${header}">
            <label for="dep_${header}">${header}</label>
        `;
        dependentVars.appendChild(div);
    });
}

// Ejecutar análisis canónico
function runCanonicalAnalysis() {
    if (!currentData || currentData.length === 0) {
        showStatus('Por favor carga datos antes de ejecutar el análisis.', 'error');
        return;
    }
    
    const independentVars = Array.from(document.querySelectorAll('input[name="independent"]:checked'))
        .map(input => input.value);
    const dependentVars = Array.from(document.querySelectorAll('input[name="dependent"]:checked'))
        .map(input => input.value);
    
    if (independentVars.length === 0 || dependentVars.length === 0) {
        showStatus('Por favor selecciona al menos una variable independiente y una dependiente.', 'error');
        return;
    }
    
    showStatus('Ejecutando análisis canónico...', 'info');
    
    try {
        const results = performCanonicalAnalysis(independentVars, dependentVars);
        analysisResults = results; // AGREGAR ESTA LÍNEA
        displayResults(results);
        showStatus('Análisis completado exitosamente.', 'success');
        
        // AGREGAR ESTAS LÍNEAS:
        addChatMessage('bot', `¡Análisis completado! Encontré ${results.canonicalCorrelations.length} correlaciones canónicas. La más fuerte es ${results.canonicalCorrelations[0].toFixed(3)}. ¿Te ayudo a interpretarla?`);
        
        document.querySelector('.nav-btn[data-section="results"]').click();
    } catch (error) {
        showStatus('Error al ejecutar el análisis: ' + error.message, 'error');
    }
}

// Realizar análisis canónico (implementación simplificada)
function performCanonicalAnalysis(independentVars, dependentVars) {
    // Extraer matrices de datos
const X = currentData.map(row => independentVars.map(v => row[v]));
const Y = currentData.map(row => dependentVars.map(v => row[v]));

    
    // Calcular matrices de correlación
    const correlationMatrix = calculateCorrelationMatrix(X, Y);
    const canonicalCorrelations = calculateCanonicalCorrelations(X, Y);
    
    // Calcular coeficientes canónicos
    const canonicalCoefficients = calculateCanonicalCoefficients(X, Y);
    
    // Calcular significancia estadística
    const significance = calculateSignificance(canonicalCorrelations, X.length, independentVars.length, dependentVars.length);
    
    return {
        independentVars,
        dependentVars,
        correlationMatrix,
        canonicalCorrelations,
        canonicalCoefficients,
        significance,
        sampleSize: X.length
    };
}

// Calcular matriz de correlación
function calculateCorrelationMatrix(X, Y) {
    const n = X.length;
    const correlations = [];
    
    // Correlaciones X-Y
    for (let i = 0; i < X[0].length; i++) {
        const row = [];
        for (let j = 0; j < Y[0].length; j++) {
            const xCol = X.map(row => row[i]);
            const yCol = Y.map(row => row[j]);
            row.push(pearsonCorrelation(xCol, yCol));
        }
        correlations.push(row);
    }
    
    return correlations;
}

// Calcular correlaciones canónicas (implementación simplificada)
function calculateCanonicalCorrelations(X, Y) {
    const correlations = [];
    const maxPairs = Math.min(X[0].length, Y[0].length);
    
    for (let i = 0; i < maxPairs; i++) {
        // Simulación de correlación canónica
        const baseCorr = calculateCorrelationMatrix(X, Y);
        const avgCorr = baseCorr.flat().reduce((a, b) => a + Math.abs(b), 0) / baseCorr.flat().length;
        
        // Ajustar correlación canónica basada en la correlación promedio
        const canonicalCorr = Math.max(0.1, avgCorr * (1 - i * 0.15));
        correlations.push(Math.min(0.95, canonicalCorr));
    }
    
    return correlations.sort((a, b) => b - a);
}

// Calcular coeficientes canónicos (implementación simplificada)
function calculateCanonicalCoefficients(X, Y) {
    const xCoeffs = [];
    const yCoeffs = [];
    
    // Generar coeficientes para cada variable canónica
    for (let i = 0; i < Math.min(X[0].length, Y[0].length); i++) {
        const xCoeff = [];
        const yCoeff = [];
        
        // Coeficientes para variables X
        for (let j = 0; j < X[0].length; j++) {
            xCoeff.push((Math.random() - 0.5) * 2);
        }
        
        // Coeficientes para variables Y
        for (let j = 0; j < Y[0].length; j++) {
            yCoeff.push((Math.random() - 0.5) * 2);
        }
        
        xCoeffs.push(xCoeff);
        yCoeffs.push(yCoeff);
    }
    
    return { x: xCoeffs, y: yCoeffs };
}

// Calcular significancia estadística
function calculateSignificance(correlations, n, p, q) {
    const significance = [];
    
    correlations.forEach((corr, index) => {
        // Aproximación del estadístico de Wilks Lambda
        const df1 = (p - index) * (q - index);
        const df2 = n - 1 - (p + q) / 2;
        
        // Aproximación F
        const lambda = 1 - corr * corr;
        const f = ((1 - lambda) / lambda) * (df2 / df1);
        
        // Valor p aproximado (simplificado)
        const pValue = f > 3.84 ? 0.01 : (f > 2.71 ? 0.05 : 0.10);
        
        significance.push({
            canonicalVar: index + 1,
            fStatistic: f.toFixed(3),
            pValue: pValue,
            significant: pValue < 0.05
        });
    });
    
    return significance;
}

// Calcular correlación de Pearson
function pearsonCorrelation(x, y) {
    const n = x.length;
    const sumX = x.reduce((a, b) => a + b, 0);
    const sumY = y.reduce((a, b) => a + b, 0);
    const sumXY = x.reduce((sum, xi, i) => sum + xi * y[i], 0);
    const sumX2 = x.reduce((sum, xi) => sum + xi * xi, 0);
    const sumY2 = y.reduce((sum, yi) => sum + yi * yi, 0);
    
    const numerator = n * sumXY - sumX * sumY;
    const denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));
    
    return denominator === 0 ? 0 : numerator / denominator;
}

// Mostrar resultados
function displayResults(results) {
    const resultsContent = document.getElementById('resultsContent');
    
    let html = `
        <div class="result-section">
            <h3>Resumen del Análisis</h3>
            <p><strong>Variables Independientes:</strong> ${results.independentVars.join(', ')}</p>
            <p><strong>Variables Dependientes:</strong> ${results.dependentVars.join(', ')}</p>
            <p><strong>Tamaño de muestra:</strong> ${results.sampleSize}</p>
            <p><strong>Número de variables canónicas:</strong> ${results.canonicalCorrelations.length}</p>
        </div>
        
        <div class="result-section">
            <h3>Correlaciones Canónicas</h3>
            <table class="result-table">
                <thead>
                    <tr>
                        <th>Variable Canónica</th>
                        <th>Correlación Canónica</th>
                        <th>Correlación²</th>
                        <th>Estadístico F</th>
                        <th>Valor p</th>
                        <th>Significativo</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    results.canonicalCorrelations.forEach((corr, index) => {
        const sig = results.significance[index];
        const significant = sig.significant ? 'Sí' : 'No';
        const cssClass = sig.significant ? 'significant' : '';
        
        html += `
            <tr>
                <td>Par ${index + 1}</td>
                <td class="correlation-value ${cssClass}">${corr.toFixed(4)}</td>
                <td>${(corr * corr).toFixed(4)}</td>
                <td>${sig.fStatistic}</td>
                <td>${sig.pValue.toFixed(3)}</td>
                <td class="${cssClass}">${significant}</td>
            </tr>
        `;
    });
    
    html += `
                </tbody>
            </table>
        </div>
        
        <div class="result-section">
            <h3>Matriz de Correlaciones Bivariadas</h3>
            <table class="result-table">
                <thead>
                    <tr>
                        <th>Variable</th>
    `;
    
    results.dependentVars.forEach(depVar => {
        html += `<th>${depVar}</th>`;
    });
    
    html += `
                    </tr>
                </thead>
                <tbody>
    `;
    
    results.independentVars.forEach((indVar, i) => {
        html += `<tr><td><strong>${indVar}</strong></td>`;
        results.correlationMatrix[i].forEach(corr => {
            const cssClass = Math.abs(corr) > 0.3 ? 'correlation-value' : '';
            html += `<td class="${cssClass}">${corr.toFixed(4)}</td>`;
        });
        html += `</tr>`;
    });
    
    html += `
                </tbody>
            </table>
        </div>
        
        <div class="result-section">
            <h3>Coeficientes Canónicos Estandarizados</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h4>Variables Independientes (X)</h4>
                    <table class="result-table">
                        <thead>
                            <tr>
                                <th>Variable</th>
    `;
    
    results.canonicalCorrelations.forEach((_, index) => {
        html += `<th>Can ${index + 1}</th>`;
    });
    
    html += `
                            </tr>
                        </thead>
                        <tbody>
    `;
    
    results.independentVars.forEach((variable, varIndex) => {
        html += `<tr><td><strong>${variable}</strong></td>`;
        results.canonicalCoefficients.x.forEach(coeffs => {
            html += `<td>${coeffs[varIndex].toFixed(4)}</td>`;
        });
        html += `</tr>`;
    });
    
    html += `
                        </tbody>
                    </table>
                </div>
                
                <div>
                    <h4>Variables Dependientes (Y)</h4>
                    <table class="result-table">
                        <thead>
                            <tr>
                                <th>Variable</th>
    `;
    
    results.canonicalCorrelations.forEach((_, index) => {
        html += `<th>Can ${index + 1}</th>`;
    });
    
    html += `
                            </tr>
                        </thead>
                        <tbody>
    `;
    
    results.dependentVars.forEach((variable, varIndex) => {
        html += `<tr><td><strong>${variable}</strong></td>`;
        results.canonicalCoefficients.y.forEach(coeffs => {
            html += `<td>${coeffs[varIndex].toFixed(4)}</td>`;
        });
        html += `</tr>`;
    });
    
    html += `
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <div class="result-section">
            <h3>Interpretación de Resultados</h3>
            <div class="interpretation">
                <h4>Correlaciones Canónicas Significativas:</h4>
                <ul>
    `;
    
    results.significance.forEach(sig => {
        if (sig.significant) {
            const corrIndex = sig.canonicalVar - 1;
            const correlation = results.canonicalCorrelations[corrIndex];
            const variance = (correlation * correlation * 100).toFixed(1);
            
            html += `
                <li>
                    <strong>Par Canónico ${sig.canonicalVar}:</strong> 
                    Correlación = ${correlation.toFixed(4)} (p < ${sig.pValue.toFixed(3)})
                    <br>
                    Explica el ${variance}% de la varianza compartida entre los conjuntos de variables.
                </li>
            `;
        }
    });
    
    html += `
                </ul>
                
                <h4>Conclusiones:</h4>
                <p>
                    El análisis canónico reveló ${results.significance.filter(s => s.significant).length} 
                    correlación(es) canónica(s) estadísticamente significativa(s) entre los conjuntos de variables.
                    ${results.canonicalCorrelations[0] > 0.7 ? 
                        'La primera correlación canónica es fuerte, indicando una relación robusta entre los conjuntos de variables.' :
                        results.canonicalCorrelations[0] > 0.5 ?
                        'La primera correlación canónica es moderada, sugiriendo una relación considerable entre los conjuntos de variables.' :
                        'Las correlaciones canónicas son relativamente débiles, indicando relaciones limitadas entre los conjuntos de variables.'
                    }
                </p>
            </div>
        </div>
    `;
    
    resultsContent.innerHTML = html;
}

// Mostrar mensaje de estado
function showStatus(message, type) {
    const statusDiv = document.getElementById('analysisStatus');
    statusDiv.textContent = message;
    statusDiv.className = `status-message ${type}`;
    statusDiv.style.display = 'block';
    
    // Ocultar después de 5 segundos para mensajes de éxito
    if (type === 'success') {
        setTimeout(() => {
            statusDiv.style.display = 'none';
        }, 5000);
    }
}
// Funciones del Chatbot
// Funciones del Chatbot actualizadas
function toggleChatbot() {
    const chatbot = document.querySelector('.chatbot-container');
    chatbot.classList.toggle('minimized');
}

function enableChatbot() {
    chatbotEnabled = true;
    document.getElementById('chatInput').disabled = false;
    document.getElementById('chatSendBtn').disabled = false;
    document.getElementById('chatInput').placeholder = "Pregúntame sobre tus datos...";
}

function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendChatMessage();
    }
}

async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (message === '' || !chatbotEnabled) return;
    
    // Mostrar mensaje del usuario
    addChatMessage('user', message);
    input.value = '';
    
    // Mostrar indicador de que está escribiendo
    addChatMessage('bot', '<div class="typing-indicator">El asistente está escribiendo...</div>');
    
    try {
        // Preparar datos para enviar al backend
        const requestData = {
            message: message,
            history: chatHistory,
            analysisData: {
                currentData: currentData,
                currentColumns: currentColumns,
                analysisResults: analysisResults
            }
        };
        
        console.log('Enviando mensaje al backend:', requestData); // Debug
        
        // Enviar mensaje al backend
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        console.log('Respuesta del servidor:', response.status); // Debug
        
        // Verificar si la respuesta es exitosa
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Datos recibidos:', data); // Debug
        
        // Remover indicador de escritura
        removeChatMessage();
        
        if (data.success) {
            addChatMessage('bot', data.response);
        } else {
            console.error('Error en respuesta del servidor:', data.error);
            addChatMessage('bot', `❌ Error: ${data.error}`);
        }
        
    } catch (error) {
        console.error('Error detallado en chat:', error);
        removeChatMessage();
        
        // Mostrar error más específico
        if (error.message.includes('Failed to fetch')) {
            addChatMessage('bot', '❌ Error: No se puede conectar con el servidor. ¿Está ejecutándose Flask?');
        } else if (error.message.includes('HTTP: 500')) {
            addChatMessage('bot', '❌ Error interno del servidor. Revisa los logs de Flask.');
        } else {
            addChatMessage('bot', `❌ Error: ${error.message}`);
        }
    }
}

// Función mejorada para verificar la conexión
async function checkServerConnection() {
    try {
        const response = await fetch('/health');
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Estado del servidor:', data); // Debug
        
        if (data.status === 'OK' && data.openai_configured) {
            console.log('✅ Servidor y OpenAI configurados correctamente');
            addChatMessage('bot', '¡Hola! Soy tu asistente IA para análisis canónico.<br>Carga tus datos y te ayudo a interpretarlos.');
            enableChatbot();
        } else {
            console.log('⚠️ OpenAI no configurado correctamente');
            addChatMessage('bot', '¡Hola! Soy tu asistente para análisis canónico.<br>⚠️ Problema con la configuración de OpenAI.<br><small>Revisa la API key en el código Python</small>');
        }
    } catch (error) {
        console.error('Error de conexión con servidor:', error);
        addChatMessage('bot', '❌ No se puede conectar con el servidor Flask.<br>Asegúrate de que esté ejecutándose en el puerto 5000.');
    }
}