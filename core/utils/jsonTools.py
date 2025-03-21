def complex_to_json(z):
    if isinstance(z, complex):
        return {'real': z.real, 'imag': z.imag}
    else:
        type_name = z.__class__.__name__
        raise TypeError(
            f"Object of type '{type_name}' is not JSON serializable")


def complex_matrix_to_json(complex_matrix):
    jsonList = []
    jsonListAux = []
    if not isinstance(complex_matrix, list):
        complex_matrix = complex_matrix.tolist()
    for cmplist in complex_matrix:
        for cmp in cmplist:
            jsonListAux.append(complex_to_json(cmp))
        jsonList.append(jsonListAux)
        jsonListAux = []
    return jsonList


def json_to_complex(dct):
    if 'real' in dct and 'imag' in dct:
        return complex(dct['real'], dct['imag'])
    return dct


def json_matrix_to_complex(json_matrix):
    listComplex = []
    listComplexAux = []
    for dct in json_matrix:
        for d in dct:
            listComplexAux.append(json_to_complex(d))
        listComplex.append(listComplexAux)
        listComplexAux = []
    return listComplex


def convert_cytoscape_to_decimal(graph_data):
    def convert_to_decimal(binary_tuple):
        # converts binary tuple to decimal
        return str(sum(bit << i for i,
                       bit in enumerate(reversed(binary_tuple))))

    decimal_graph = graph_data.copy()

    # Check if the graph_data is already in decimal format
    for node in decimal_graph['elements']['nodes']:
        node_id = node['data']['id']
        if not node_id.isdigit():
            break
    else:
        # If the data is already in decimal format, return it as it is
        return decimal_graph

    # To store the mapping of original binary node IDs to decimal node
    # IDs
    node_id_map = {}

    for node in decimal_graph['elements']['nodes']:
        node_id = tuple(
            map(int, node['data']['id'].strip('()').split(', ')))
        decimal_id = convert_to_decimal(node_id)
        node['data']['id'] = decimal_id
        node_id_map[node_id] = decimal_id

        node_value = tuple(map(int, node['data']['value']))
        decimal_value = convert_to_decimal(node_value)
        node['data']['value'] = decimal_value

        node_name = tuple(
            map(int, node['data']['name'].strip('()').split(', ')))
        decimal_name = convert_to_decimal(node_name)
        node['data']['name'] = decimal_name

    for edge in decimal_graph['elements']['edges']:
        source = edge['data']['source']
        target = edge['data']['target']
        decimal_source = node_id_map[source]
        decimal_target = node_id_map[target]
        edge['data']['source'] = decimal_source
        edge['data']['target'] = decimal_target

    return decimal_graph
