import pandas as pd

impactos_df = pd.read_excel("Impactos.xlsx")
impactos_dict = impactos_df.to_dict(orient="records")

celdas_df = pd.read_excel("Celdas.xlsx")

celdas_map = {}
for _, row in celdas_df.iterrows():
    celdas_map[row["Código"]] = {
        "Latitud": row["Latitud"],
        "Longitud": row["Longitud"],
        "Radio de Cobertura": row["Radio de Cobertura"]
    }

for impacto in impactos_dict:
    if impacto["Celda"] in celdas_map:  # Acceso directo al valor "Celdas"
        impacto["Latitud"] = celdas_map[impacto["Celda"]]["Latitud"]
        impacto["Longitud"] = celdas_map[impacto["Celda"]]["Longitud"]
        impacto["Radio"] = celdas_map[impacto["Celda"]]["Radio de Cobertura"]
    else:
        impacto["Latitud"] = None
        impacto["Longitud"] = None
        impacto["Radio"] = None

output_df = pd.DataFrame(impactos_dict)
output_df.to_excel("Impactos_con_celdas.xlsx", index=False)

print("Done!")
