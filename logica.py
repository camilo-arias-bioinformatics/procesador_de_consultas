def calcular_promedios(df):
    promedios = {
        "variable_1": df["variable_1"].mean(),
        "variable_2": df["variable_2"].mean()
    }
    return promedios
