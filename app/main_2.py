from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Importar funciones y conjunto de datos desde el script utils.py
from app.utils import players_info, country_max_goals ,countries_goals, top_scorers , teams_goals , df

# Crear la instancia de FastAPI
app = FastAPI()

# Modelo de Pydantic para la validación de datos
class Player(BaseModel):
    name: str
    team: str
    country: str
    team_nationality: str
    goals: int
    penalty_goals: int

# Decoradores:

# Decorador URL raíz (/)
# Trae el primer mensaje
@app.get("/")
def read_root():
    return {"Hola": "Mundo"}

# Decorador para la ruta [http://dominio.com/players/]
# Trae datos de todos los jugadores
@app.get("/players/")
def read_players():
    return df.to_dict(orient='records')

# Decorador para la ruta [http://dominio.com/players/{player_name}]
# Trae información de un jugador específico basándose en el nombre proporcionado en la URL.
@app.get("/players/{player_name}")
def read_player(player_name: str):
    player_data = players_info(player_name)
    if player_data: # Comprueba si la función jugadores_info devolvió datos válidos.
        return player_data
    else:
        return {"error": "Player not found"}

# Decorador para la ruta [http://dominio.com/country/max_goals]
@app.get("/country/max_goals")
def read_country_max_goals():
    return country_max_goals()

# Decorador para la ruta [http://dominio.com/countries/goals]
@app.get("/countries/goals")
def read_countries_goals():
    return countries_goals()

# Decorador para la ruta [http://dominio.com/teams/goals]
@app.get("/teams/goals")
def read_teams_goals():
    return teams_goals()


@app.get("/top_scorers/{option}")
def read_top_scorers(option: str):
    return top_scorers(option)

# Corremos el aplicativo en un portal de uvicorn, en el localhost y en el puerto 8000
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)