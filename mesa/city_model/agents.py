import mesa
from mesa import Agent
from pruebitaBFS import generate_route #import function to generate the full path the agent should follows
#TODO not obeying the semaphores

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
        self.route = generate_route((9,1), (6,5)) #TODO this should come from the model, as start and end

    def step(self):
        """Perform one step in the simulation."""
        if self.route:
            # Get the next position in the route
            next_position = self.route.pop(0)  # Remove and get the first step
            # Move the agent to the next position
            self.model.grid.move_agent(self, next_position)
            # Update current position
            self.current_position = next_position
            print(f"Moved to {next_position}. Remaining route: {self.route}")

        else:
            # Route is empty, the car has reached its destination
            self.parked = True
            print("Car is parked. Route complete.")


