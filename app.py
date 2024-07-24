from flask import Flask, render_template, request, jsonify
from analysis import count_words_in_tokens, lexical_analysis, syntactic_analysis, semantic_analysis, find_reserved_words, graph_to_json
import os
import io
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.form['code']
    tokens = lexical_analysis(code)
    parse_tree = syntactic_analysis(tokens)
    semantic_errors = semantic_analysis(tokens)
    word_count, words = count_words_in_tokens(tokens)
    reserved_words = find_reserved_words(tokens)
    tree_json = graph_to_json(parse_tree)
    
    return jsonify({
        'tokens': tokens,
        'parse_tree': tree_json,
        'semantic_errors': semantic_errors,
        'word_count': word_count,
        'words': words,
        'reserved_words': reserved_words
    })

@app.route('/execute', methods=['POST'])
def execute():
    code = request.form['code']

    # Capturar la salida del código ejecutado
    old_stdout = sys.stdout  # Guarda el estándar de salida actual
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    
    execution_output = ''
    execution_error = ''
    
    try:
        # Ejecutar el código en un entorno seguro, pero con `__builtins__` para permitir acceso a funciones estándar
        local_vars = {}
        exec(code, {"__builtins__": __builtins__}, local_vars)  # Ejecutar el código con un entorno más abierto
        execution_output = new_stdout.getvalue()
    except Exception as e:
        execution_error = str(e)
    
    # Restaurar el estándar de salida original
    sys.stdout = old_stdout

    return jsonify({
        'execution_output': execution_output,
        'execution_error': execution_error
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=False, use_reloader=False)
