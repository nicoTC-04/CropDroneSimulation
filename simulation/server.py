import mesa
from .model import DroneModel, DroneAgent, CropAgent

COLORS = {"Drone": "#0000FF", "Crop": "#00FF00", "Collected": "#555555"}
EMOJI = {"Drone": "🚁", "Crop": "🌾", "Collected": "✔️"}

def portrayal(agent):
    if isinstance(agent, DroneAgent):
        return {
            "Shape": "circle",
            "r": 0.5,
            "Filled": "true",
            "Layer": 1,
            "Color": COLORS["Drone"],
            "text": EMOJI["Drone"],
            "text_color": "white",
        }
    elif isinstance(agent, CropAgent):
        return {
            "Shape": "rect",
            "w": 0.8,
            "h": 0.8,
            "Filled": "true",
            "Layer": 0,
            "Color": COLORS["Collected"] if agent.collected else COLORS["Crop"],
            "text": EMOJI["Collected"] if agent.collected else EMOJI["Crop"],
            "text_color": "black",
        }

canvas_element = mesa.visualization.CanvasGrid(portrayal, 20, 20, 500, 500)

model_params = {
    "width": 20,
    "height": 20,
    "num_drones": mesa.visualization.Slider("Number of Drones", 3, 1, 10, 1),
    "num_crops": mesa.visualization.Slider("Number of Crops", 10, 1, 50, 1),
}

server = mesa.visualization.ModularServer(
    DroneModel, [canvas_element], "Recoleccion de cultivo", model_params, port=1734
)

server.launch()
