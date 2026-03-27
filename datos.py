import pandas as pd

def cargar_datos():
    df = pd.read_csv("data/data.csv")
    return df
