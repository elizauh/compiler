import re
import keyword
import networkx as nx
import json

def lexical_analysis(code):
    tokens = re.findall(r'\w+|[^\s\w]', code)
    return tokens

def syntactic_analysis(tokens):
    parse_tree = nx.DiGraph()
    parse_tree.add_edges_from([(tokens[i], tokens[i+1]) for i in range(len(tokens)-1)])
    return parse_tree

def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def semantic_analysis(tokens):
    semantic_errors = []
    variables = set()
    functions = set()
    conditionals = {'if', 'elif', 'else'}
    loops = {'while'}
    operators = { '+', '-', '*', '/', '%', '**', '//'}
    comparators = {'<', '>', '<=', '>=', '==', '!='}
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if token == '=':
            if tokens[i-1] not in variables:
                pass
            elif i + 1 >= len(tokens) or tokens[i + 1] == '':
                semantic_errors.append(f"Error: se debe asignar un valor a la variable '{tokens[i-1]}'.")

        elif token == 'def':
            if i + 2 < len(tokens) and tokens[i + 1].isidentifier() and tokens[i + 2] == '(':
                function_name = tokens[i + 1]
                open_paren_index = tokens.index('(', i + 2)
                close_paren_index = tokens.index(')', open_paren_index)
                if close_paren_index > open_paren_index + 1:
                    function_body = tokens[close_paren_index + 1]
                    if function_body != ':':
                        semantic_errors.append(f"Error: falta el cuerpo de la función '{function_name}'.")
                    else:
                        functions.add(function_name)
                        # Verificar cambios dentro del cuerpo de la función
                        function_tokens = tokens[close_paren_index + 2:]
                        if function_name == 'es_primo':  # Nombre de la función específica
                            expected_tokens = lexical_analysis("if numero <= 1: return False for i in range(2, int(numero**0.5) + 1): if numero % i == 0: return False return True")
                            if function_tokens != expected_tokens:
                                semantic_errors.append(f"Error: cambio detectado en el cuerpo de la función '{function_name}'.")
                else:
                    semantic_errors.append(f"Error: falta el cuerpo de la función '{function_name}'.")

        elif token.isidentifier():
            if token in keyword.kwlist:
                if token in conditionals or token in loops:
                    if i > 0 and tokens[i-1] != ':' and tokens[i-1] not in variables and tokens[i-1] not in functions:
                        semantic_errors.append(f"Error: '{token}' es una palabra reservada y no puede ser usada como identificador.")
            elif token not in variables and token not in functions:
                if i + 1 < len(tokens) and tokens[i + 1] == '=':
                    if i + 2 < len(tokens) and tokens[i + 2] == '':
                        semantic_errors.append(f"Error: se debe asignar un valor a la variable '{token}'.")
                    variables.add(token)
                elif i + 1 < len(tokens) and tokens[i + 1] == '(':
                    functions.add(token)
                elif i > 0 and tokens[i - 1] == '=':
                    if not is_number(tokens[i + 1]):
                        semantic_errors.append(f"Error: se debe asignar un valor numérico a la variable '{tokens[i - 1]}'.")

        elif token in operators:
            if token == '=':
                if tokens[i-1] not in variables:
                    semantic_errors.append(f"Error: variable '{tokens[i-1]}' no declarada.")
                elif i + 1 >= len(tokens) or tokens[i + 1] == '':
                    semantic_errors.append(f"Error: se debe asignar un valor a la variable '{tokens[i-1]}'.")

        elif token in comparators:
            if tokens[i-1] not in variables and tokens[i-1] not in functions:
                semantic_errors.append(f"Error: variable '{tokens[i-1]}' no declarada.")
        
        i += 1
    
    return semantic_errors

def find_reserved_words(tokens):
    reserved_words = set(keyword.kwlist)
    found_words = [token for token in tokens if token in reserved_words]
    return found_words

def graph_to_json(graph):
    data = nx.node_link_data(graph)
    return json.dumps(data)


def count_words_in_tokens(tokens):
    words = [token for token in tokens if token.isalpha()]
    word_count = len(words)
    return word_count, words
