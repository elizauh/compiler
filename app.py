from flask import Flask, render_template, request, jsonify
from analysis import count_words_in_tokens, lexical_analysis, syntactic_analysis, semantic_analysis, find_reserved_words, graph_to_json
import os
import io
import sys
import subprocess

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
    
    # Crear un archivo en memoria
    code_file = io.StringIO(code)
    
    # Capturar la salida del código ejecutado
    execution_output = ''
    execution_error = ''
    
    try:
        # Usar subprocess para ejecutar el código Python
        process = subprocess.Popen(
            ['python', '-c', code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(timeout=30)  # Tiempo máximo de ejecución en segundos
        
        execution_output = stdout
        execution_error = stderr
    except subprocess.TimeoutExpired as e:
        execution_error = f"Timeout Expired: {str(e)}"
    except Exception as e:
        execution_error = f"Error: {str(e)}"
    
    return jsonify({
        'execution_output': execution_output,
        'execution_error': execution_error
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=False, use_reloader=False)