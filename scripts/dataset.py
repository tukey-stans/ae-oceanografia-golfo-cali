import pandas as pd
from pathlib import Path
from unidecode import unidecode
import os


ruta_actual = Path.cwd()
PROJECT_DIR = ruta_actual
RAW_DIR     = PROJECT_DIR / 'data' / 'raw'
PROC_DIR     = PROJECT_DIR / 'data' / 'processed'

os.makedirs(PROC_DIR,exist_ok=True)


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza nombres de columnas y acorta 'estacion_del_ano' y 'evento_interanual'.
    """
    # 1) Normalizar: quita tildes, espacios, pone minúsculas y guiones bajos
    df = df.rename(columns=lambda x: (
        unidecode(x)
        .strip()
        .lower()
        .replace(' ', '_')
    ))
    # 2) Acortar nombres específicos
    df = df.rename(columns={
        'estacion_del_ano':  'estacion',
        'evento_interanual': 'evento'
    })
    return df



print("Leyendo y cargando datos...")
tsm = pd.read_excel(RAW_DIR / 'Base de datos TSM consultoria estadística.xlsx')
chla = pd.read_excel(RAW_DIR / 'Base de datos Chla consultoria estadística.xlsx')
coordenadas = pd.read_csv(RAW_DIR / 'Coordenadas zona costera occidental GC.csv', header=None, names=['longitud', 'hola', 'latitud'], index_col=False)
coordenadas =  coordenadas.drop("hola", axis=1)

oni = pd.read_csv(RAW_DIR / 'oni-Cold & Warm Episodes by Season.csv - Sheet1.csv')

tsm.columns = tsm.columns.str.strip().str.replace('°', '', regex=False)
chla.columns = chla.columns.str.strip().str.replace('°', '', regex=False)


oni = oni[oni['Year'].apply(lambda x: str(x).isdigit())].copy()
oni['Year'] = oni['Year'].astype(int)

# Formato largo
oni_long = oni.melt(id_vars='Year', var_name='Season', value_name='ONI')

# Mapeo estaciones móviles a meses
season_to_month = {
    'DJF': 1, 'JFM': 2, 'FMA': 3, 'MAM': 4,
    'AMJ': 5, 'MJJ': 6, 'JJA': 7, 'JAS': 8,
    'ASO': 9, 'SON': 10, 'OND': 11, 'NDJ': 12
}
oni_long['Month'] = oni_long['Season'].map(season_to_month)

# Crear columna de fecha
oni_long['Fecha'] = pd.to_datetime(dict(year=oni_long['Year'],
                                        month=oni_long['Month'],
                                        day=15))

print("<<  Datos cargados correctamente!   >>")



# Limpiar y ordenar
print("Limpiando y ordenando datos...")
oni_long = oni_long[['Fecha', 'ONI']].dropna().sort_values('Fecha').reset_index(drop=True)

# --- Alinear FECHAS para hacer merge ---
# Convertir FECHA a periodo mensual (año-mes) para tsm y chla
tsm['FECHA'] = pd.to_datetime(tsm['FECHA']).dt.to_period('M').dt.to_timestamp()
chla['FECHA'] = pd.to_datetime(chla['FECHA']).dt.to_period('M').dt.to_timestamp()
oni_long['Fecha'] = oni_long['Fecha'].dt.to_period('M').dt.to_timestamp()

# --- Merge de datos ---
merged_tsm = pd.merge(tsm, oni_long, left_on='FECHA', right_on='Fecha', how='inner')
merged_chla = pd.merge(chla, oni_long, left_on='FECHA', right_on='Fecha', how='inner')
merged_tsm = merged_tsm.drop("Fecha", axis=1)
merged_chla = merged_chla.drop("Fecha", axis=1)


try:
    # Limpia ambos DataFrames
    merged_tsm  = clean_df(merged_tsm)
    merged_chla = clean_df(merged_chla)

except Exception as e:
    print("❌ Ocurrió un error al normalizar los DataFrames:", e)


print("Ordenando columnas...")

tsm_long = pd.melt(
    merged_tsm,
    id_vars=['fecha', 'evento', 'oni'],
    value_vars=[col for col in merged_tsm.columns if col.startswith('est_')],
    var_name='estacion',
    value_name='tsm'
)
tsm_long['fecha'] = pd.to_datetime(tsm_long['fecha'])

# PASO 2: Convertir CHLA a formato largo
meses_es_a_num = {
    "Enero": "01", "Febrero": "02", "Marzo": "03", "Abril": "04",
    "Mayo": "05", "Junio": "06", "Julio": "07", "Agosto": "08",
    "Septiembre": "09", "Octubre": "10", "Noviembre": "11", "Diciembre": "12"
}

chla_long = pd.melt(
    merged_chla,
    id_vars=['ano', 'mes', 'evento', 'oni'],
    value_vars=[col for col in merged_chla.columns if col.startswith('est_')],
    var_name='estacion',
    value_name='chla'
)

# Crear columna de fecha en CHLA
chla_long['mes_num'] = chla_long['mes'].map(meses_es_a_num)
chla_long['fecha'] = pd.to_datetime(chla_long['ano'].astype(str) + '-' + chla_long['mes_num'] + '-01')

# PASO 3: Outer join por fecha y estación
combined = pd.merge(tsm_long, chla_long, on=['fecha', 'estacion'], how='outer')

# PASO 4: Extraer índice de estación
combined['est_index'] = combined['estacion'].str.extract(r'est_(\d+)').astype(float) - 1

# PASO 5: Unir coordenadas (ya cargadas como `coordenadas`)
coord_aligned = coordenadas.reindex(combined['est_index'].dropna().astype(int).values).reset_index(drop=True)
coord_aligned = coord_aligned.reindex(combined.index)
combined = pd.concat([combined.reset_index(drop=True), coord_aligned], axis=1)
combined['evento_x'] = combined['evento_x'].replace({'Normal': 'Neutro'})

# Unificar columnas duplicadas
combined['evento'] = combined['evento_x'].combine_first(combined['evento_y'])
combined['oni'] = combined['oni_x'].combine_first(combined['oni_y'])

# Eliminar columnas duplicadas
combined = combined.drop(columns=['evento_x', 'evento_y', 'oni_x', 'oni_y'])
combined['evento'] = combined['evento'].replace({'Normal': 'Neutro'})

print("<<  Datos limpiados y ordenados correctamente!  >>",end='\n')


combined.to_csv(PROC_DIR/'dataset.csv')