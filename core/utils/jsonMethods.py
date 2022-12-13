def complex_to_json(z):
    if isinstance(z, complex):
        return {'real': z.real, 'imag': z.imag}
    else:
        type_name = z.__class__.__name__
        raise TypeError(f"Object of type '{type_name}' is not JSON serializable")

def json_to_complex(dct):
    if 'real' in dct and 'imag' in dct:
        return complex(dct['real'], dct['imag'])
    return dct

def columnListJson_to_complex(listJson):
    listComplex = []
    listComplexAux = []
    for dct in listJson:
        for d in dct:
            listComplexAux.append(json_to_complex(d))
        listComplex.append(listComplexAux)
        listComplexAux = []
    return listComplex
