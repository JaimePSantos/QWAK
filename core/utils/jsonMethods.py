def complex_to_json(z):
    if isinstance(z, complex):
        return {'real': z.real, 'imag': z.imag}
    else:
        type_name = z.__class__.__name__
        raise TypeError(f"Object of type '{type_name}' is not JSON serializable")

def complex_matrix_to_json(complex_matrix):
    jsonList = []
    jsonListAux = []
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
