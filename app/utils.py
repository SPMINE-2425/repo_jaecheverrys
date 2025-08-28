import pandas as pd
import re
from unidecode import unidecode

# Asume que el script y la carpeta 'Datos' están en el mismo directorio padre
df = pd.read_csv('./Datos/goleadores.csv')

def players_info(nombre):
    """
    Devuelve la información de los jugadores.
    """
    nombre = nombre.lower()
    nombre = nombre.replace(" ", "")  # Eliminar espacios en blanco
    nombre = nombre.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")  # Normalizar tildes latinas
    nombre = re.sub(r'[^a-zA-Z]', '', nombre)  # Eliminar caracteres especiales

    df_copy = df.copy()  # Hacer una copia del DataFrame para evitar modificar el original
    df_copy['Player'] = df_copy['Player'].str.lower()  # Normalizar nombres de jugadores a minúsculas
    df_copy['Player'] = df_copy['Player'].str.replace(" ", "", regex=False)  # Eliminar espacios en blanco
    df_copy['Player'] = df_copy['Player'].apply(lambda x: unidecode(x))  # Normalizar tildes latinas
    df_copy['Player'] = df_copy['Player'].str.replace(r'[^a-zA-Z]', '', regex=True)

    # Busqueda del nombre del jugador
    df_player = df_copy[df_copy['Player'].str.contains(nombre, case=False, regex=True)]
    if df_player.empty:
        return {"error": "Player not found"}
    # Convertir el DataFrame filtrado a un diccionario
    df_player = df.loc[df_player.index]
    df_player['Player'] = df_player['Player'].str.title()  # Formate
    df_player['Team'] = df_player['Team'].str.title()  # Formatear nombres de equipos
    df_player['Country'] = df_player['Country'].str.title()  # Formatear nombres de países
    df_player['Team Nationality'] = df_player['Team Nationality'].str.title()  # Formatear nombres de países
    df_player['Goals'] = df_player['Goals'].astype(int)  # Asegurarse de que los goles son enteros
    df_player['Penalty Goals'] = df_player['Penalty Goals'].astype(int)  # Asegurarse de que los goles de penalti son enteros
    df_player['Goals'] = df_player['Goals'].apply(lambda x: f"{x:,}")  # Formatear los goles con comas
    df_player['Penalty Goals'] = df_player['Penalty Goals'].apply(lambda x: f"{x:,}")  

    df_player = df_player[['Player', 'Team', 'Country', 'Team Nationality', 'Goals', 'Penalty Goals']]

    
    return df_player.to_dict(orient='records')

def top_scorers(option):
    """
    Devuelve los goleadores de la liga.
    """
    # Define la cantidad de jugadores a mostrar según la opción
    if option == 'top_10':
        top_n = 10
    elif option == 'top_5':
        top_n = 5
    elif option == 'top_3':
        top_n = 3
    elif option == 'top_1':
        top_n = 1
    else:
        # Devuelve un diccionario con el mensaje de error si la opción no es válida
        return {"mensaje": "Opción no válida. Por favor, elige entre 'top_10', 'top_5', 'top_3' o 'top_1'."}

    # Ordena el DataFrame y selecciona los 'N' mejores jugadores
    df_ordenado = df.sort_values(by='Goals', ascending=False)
    top_players = df_ordenado.head(top_n)

    # Devuelve la lista de diccionarios con los nombres y goles
    return top_players[['Player', 'Goals']].to_dict(orient='records')

def country_max_goals():
    """
    Devuelve el país con más goles.
    """
    max_goals = df['Goals'].max()
    country = df[df['Goals'] == max_goals]['Country'].values[0]
    return {"Country": country, "Goals": int(max_goals)}

def countries_goals():
    """
    Devuelve los goles por país.
    """
    return df.groupby('Country')['Goals'].sum().reset_index().to_dict(orient='records')

def teams_goals():
    """
    Devuelve los goles por equipo.
    """
    return df.groupby('Team')['Goals'].sum().reset_index().to_dict(orient='records')