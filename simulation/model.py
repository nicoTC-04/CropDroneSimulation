import mesa
import math

class DroneAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.has_task = False  # Indica si el dron está recolectando
        self.target = None  # Cultivo objetivo

    def step(self):
        # Si no tiene tarea, busca un cultivo cercano
        if not self.has_task:
            self.target = self.find_nearest_crop()
            if self.target:
                self.has_task = True
        else:
            # Si tiene un objetivo, moverse hacia él
            self.move_towards_target()

    def find_nearest_crop(self):
        # Busca el cultivo más cercano en el grid
        nearest_crop = None
        shortest_distance = float('inf')
        for agent in self.model.schedule.agents:
            if isinstance(agent, CropAgent) and not agent.collected:
                distance = self.get_distance(self.pos, agent.pos)
                if distance < shortest_distance:
                    shortest_distance = distance
                    nearest_crop = agent
        return nearest_crop

    def move_towards_target(self):
        if self.target and not self.target.collected:
            # Calcular la dirección hacia el objetivo
            dx = self.target.pos[0] - self.pos[0]
            dy = self.target.pos[1] - self.pos[1]
            move_x = int(math.copysign(1, dx)) if dx != 0 else 0
            move_y = int(math.copysign(1, dy)) if dy != 0 else 0
            new_position = (self.pos[0] + move_x, self.pos[1] + move_y)

            # Mover el dron en el grid
            self.model.grid.move_agent(self, new_position)

            # Si llega al cultivo, recolectarlo
            if new_position == self.target.pos:
                self.target.collected = True
                self.has_task = False
                self.target = None

    @staticmethod
    def get_distance(pos1, pos2):
        # Calcula la distancia euclidiana entre dos posiciones
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


class CropAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.collected = False  # Indica si el cultivo ha sido recolectado

class DroneModel(mesa.Model):
    def __init__(self, width, height, num_drones, num_crops):
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.schedule = mesa.time.RandomActivation(self)

        # Crear drones
        for i in range(num_drones):
            drone = DroneAgent(i, self)
            self.schedule.add(drone)
            x, y = self.random.randint(0, width - 1), self.random.randint(0, height - 1)
            self.grid.place_agent(drone, (x, y))

        # Crear cultivos
        for i in range(num_drones, num_drones + num_crops):
            crop = CropAgent(i, self)
            self.schedule.add(crop)
            x, y = self.random.randint(0, width - 1), self.random.randint(0, height - 1)
            self.grid.place_agent(crop, (x, y))

        self.running = True

    def step(self):
        self.schedule.step()
