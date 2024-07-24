document.getElementById('codeForm').addEventListener('submit', async function (event) {
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


async function executeCode() {
    const code = editor.getValue();

    const response = await fetch('/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'code': code
        })
    });

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    const result = await response.json();
    console.log('Result:', result); // Log result to check structure

    
        document.getElementById('execution_output').innerHTML = `<h3>Resultado de ejecución</h3><p>${await result.execution_output}</p>`;
        document.getElementById('execution_error').innerHTML = `<h3>Errores en la ejecución</h3><p>${await result.execution_error}</p>`;
    
}

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

// Código esperado
const expectedCode = [
    "def es_primo(numero):",
    "    if numero <= 1:",
    "        return False",
    "    for i in range(2, int(numero**0.5) + 1):",
    "        if numero % i == 0:",
    "            return False",
    "    return True",
    "",
    "def imprimir_primos(n):",
    "    contador = 0",
    "    numero = 2",
    "    while contador < n:",
    "        if es_primo(numero):",
    "            print(numero, end=\" \")",
    "            contador += 1",
    "        numero += 1",
    "",
    "def main():",
    "",
    "    n = int(input(\"Introduce la cantidad de números primos que deseas imprimir: \"))",
    "",
    "    if n <= 0:",
    "        print(\"Por favor, introduce un número entero positivo.\")",
    "        return",
    "",
    "    print(f\"\\nLos primeros {n} números primos son:\")",
    "    imprimir_primos(n)",
    "    print()",
    "",
    "main()"
];

function validarCodigo() {
    const code = editor.getValue();
    const lines = code.split('\n');
    const errores = [];

    for (let i = 0; i < expectedCode.length; i++) {
        if (i >= lines.length || lines[i].trim() !== expectedCode[i].trim()) {
            errores.push(`Error en línea ${i + 1}: esperado "${expectedCode[i]}", encontrado "${lines[i] || ""}"`);
        }
    }

    const resultadoDiv = document.getElementById('resultado');
    if (errores.length === 0) {
        resultadoDiv.innerHTML = `<p>¡Código validado correctamente!</p>`;
    } else {
        resultadoDiv.innerHTML = `<p>Se encontraron errores:</p><ul>${errores.map(error => `<li>${error}</li>`).join('')}</ul>`;
    }
}

document.getElementById('validateButton').addEventListener('click', validarCodigo);

function updateLineNumbers() {
    const codeInput = document.getElementById('codeInput');
    const lineNumbers = document.getElementById('line-numbers');
    const lines = codeInput.value.split('\n').length;

    lineNumbers.innerHTML = Array.from({ length: lines }, (_, i) => `<span>${i + 1}</span>`).join('');
}

document.getElementById('codeInput').addEventListener('input', updateLineNumbers);

updateLineNumbers();
