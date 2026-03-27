def responder(pregunta, promedios):
    pregunta = pregunta.lower()

    if "variable_1" in pregunta:
        return f"El promedio de variable_1 es {promedios['variable_1']:.2f}"
    
    if "variable_2" in pregunta:
        return f"El promedio de variable_2 es {promedios['variable_2']:.2f}"
    
    if "mayor" in pregunta or "más alto" in pregunta:
        var = max(promedios, key=promedios.get)
        return f"La variable con mayor promedio es {var} con {promedios[var]:.2f}"
    
    return "No entendí la pregunta"
