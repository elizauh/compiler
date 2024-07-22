from flask import Flask, render_template, request, jsonify
from analysis import count_words_in_tokens, lexical_analysis, syntactic_analysis, semantic_analysis, find_reserved_words, graph_to_json

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

if __name__ == '__main__':
    app.run(debug=True)
