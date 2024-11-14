import mesa
from mesa import Agent

#First the traffic light agent

class TrafficLightAgent(Agent):
    """Agente que representa un semáforo con colores y control de paso."""

    def __init__(self, model, initial_color="red"):
        super().__init__(model)
        self.color = initial_color
        self.allow_pass = False if initial_color == "red" else True
        self.timer = 0

    def step(self):
        """Cambia el estado del semáforo después de ciertos pasos."""
        self.timer += 1

        if self.color == "red" and self.timer >= 10:
            self.color = "green"
            self.allow_pass = True
            self.timer = 0
        elif self.color == "green" and self.timer >= 10:
            self.color = "red"
            self.allow_pass = False
            self.timer = 0

    def display_status(self):
        """Mostrar el estado actual del semáforo."""
        print(f"Semáforo: Color={self.color}, Permite paso={self.allow_pass}")


#Then the car agent

class CarAgent(Agent):
    """Agente que representa un vehículo que puede moverse en el modelo."""
    def __init__(self, model):
        super().__init__(model)
        self.parked = False


