document.getElementById('codeForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const code = editor.getValue();
    
    const response = await fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'code': code
        })
    });
    
    const result = await response.json();
    
    displayResults(result);
});

function displayResults(result) {
    document.getElementById('tokens').innerHTML = `<h3>Tokens</h3><p>${result.tokens.join(', ')}</p>`;
    document.getElementById('wordCount').innerHTML = `<h3>Conteo de palabras</h3><p>${result.word_count}</p>`;  // Mostrar conteo de palabras
    document.getElementById('words').innerHTML = `<h3>Palabras</h3><p>${result.words.join(', ')}</p>`;
    document.getElementById('semanticErrors').innerHTML = `<h3>Semantic Errors</h3><p>${result.semantic_errors.join('<br>')}</p>`;
    document.getElementById('reservedWords').innerHTML = `<h3>Palabras Reservadas</h3><p>${result.reserved_words.join(', ')}</p>`;
    
    const parseTreeData = JSON.parse(result.parse_tree);
    const nodes = parseTreeData.nodes.map(node => ({ data: { id: node.id } }));
    const edges = parseTreeData.links.map(link => ({ data: { source: link.source, target: link.target } }));
    
    const elements = nodes.concat(edges);
    
    const cy = cytoscape({
        container: document.getElementById('parseTree'),
        elements: elements,
        style: [
            {
                selector: 'node',
                style: {
                    'background-color': '#007BFF',
                    'label': 'data(id)',
                    'text-valign': 'center',
                    'color': '#fff'
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 2,
                    'line-color': '#ccc'
                }
            }
        ],
        layout: {
            name: 'grid',
            rows: 1
        }
    });
}

// Agregar expresiones regulares para la validación del código
const regexes = [
    /^\s*def\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(\s*[a-zA-Z_][a-zA-Z0-9_]*\s*\):\s*((\{\s*[^{}]*\s*\})|([\[\(]\s*\d*\s*[\]\)]))?\s*$/,
    /^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*((\{\s*[^{}]*\s*\})|([\[\(]\s*\d*\s*[\]\)]))\s*$/,
    /^\s*[a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*\(\s*(["'a-zA-Z0-9_.,\(\)]*)\s*,\s*str\(\s*(["'a-zA-Z0-9_.,\(\)]*)\s*\)\s*\)\s*$/,
    /^\s*if\s+[a-zA-Z_][a-zA-Z0-9_]*\s*(=|==|!=|<=|>=|<|>)\s*([-+]?(?:\b\d+\b|\b\d*\.\d+\b)|[a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*$/,
    /^\s*[a-zA-Z_][a-zA-Z0-9_]*\(\s*([-+]?(?:\b\d+\b|\b\d*\.\d+\b)|[a-zA-Z_][a-zA-Z0-9_]*)\s*\)\s*$/,
    /^\s*else:\s*$/,
    /^\s*while\s+[a-zA-Z_][a-zA-Z0-9_]*\s*(==|!=|<=|>=|<|>|=)\s*([-+]?(?:\b\d+\b|\b\d*\.\d+\b|[a-zA-Z_][a-zA-Z0-9_]*))\s*:\s*$/,
    /^\s*[a-zA-Z_][a-zA-Z0-9_]*\(\s*(["'a-zA-Z0-9_.,\(\)]*)\s*\)\s*$/,
    /^\s*for\s+[a-zA-Z_][a-zA-Z0-9_]*\s+in\s+range\(\s*[a-zA-Z_][a-zA-Z0-9_]*(,\s*[a-zA-Z_][a-zA-Z0-9_]*)?\s*\)\s*:\s*$/,
    /^\s*(print|return)\(\s*[a-zA-Z_][a-zA-Z0-9_]*(,\s*[a-zA-Z_][a-zA-Z0-9_]*)?\s*\)\s*$/
];

function validarCodigo() {
    const code = editor.getValue();
    const lines = code.split('\n');
    const errores = [];

    for (let i = 0; i < lines.length; i++) {
        let matched = false;
        for (const regex of regexes) {
            if (regex.test(lines[i])) {
                matched = true;
                break;
            }
        }
        if (!matched) {
            errores.push(`Error en línea ${i + 1}: ${lines[i]}`);
        }
    }

    const resultadoDiv = document.getElementById('resultado');
    if (errores.length === 0) {
        resultadoDiv.innerHTML = '<p>El código es válido.</p>';
    } else {
        resultadoDiv.innerHTML = `<p>Se encontraron errores:</p><ul>${errores.map(error => `<li>${error}</li>`).join('')}</ul>`;
    }
}

function updateLineNumbers() {
    const codeInput = document.getElementById('codeInput');
    const lineNumbers = document.getElementById('line-numbers');
    const lines = codeInput.value.split('\n').length;

    lineNumbers.innerHTML = Array.from({ length: lines }, (_, i) => i + 1).join('\n');
}

document.getElementById('codeInput').addEventListener('input', updateLineNumbers);

updateLineNumbers();  // Inicializa los números de línea
