import mesa
from mesa import Agent
from .bfs_service import BFSService #import function to generate the full path the agent should follows

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


class CarAgent(Agent):
    """Agente que representa un vehículo que puede moverse en el modelo."""
    def __init__(self, model, start, end):
        super().__init__(model)
        self.start = start
        self.end = end
        self.parked = False
        self.bfs_service = BFSService(model, CarAgent)
        self.route = self.calculate_route(start, end)
    
    def calculate_route(self, start, end):
        route = self.bfs_service.get_route(start, end)
        if not route:
            return None
        return route[1:] # Remove the starting position from the route

    def check_semaphore_allows_pass(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos]) #with this, check if any other agent
        if len(cellmates) > 1:  # Check if there are multiple agents in the cell
            for agent in cellmates:
                # Check if the agent is of type TrafficLightAgent
                if isinstance(agent, TrafficLightAgent):
                    semaphore = agent
                    return semaphore.allow_pass        
        return True
        
    def step(self):
        """Perform one step in the simulation."""
        if self.parked:
            return

        if not self.check_semaphore_allows_pass():
            return

        if self.route:
            next_position = self.route.pop(0)  

            cellmates = self.model.grid.get_cell_list_contents([next_position])
            if any(isinstance(agent, CarAgent) for agent in cellmates) and next_position != self.end:
                self.route = self.calculate_route(self.pos, self.end)
                if not self.route:
                    return
                next_position = self.route.pop(0)

            # Move the agent to the next position
            self.model.grid.move_agent(self, next_position)
            if self.pos == self.end:
                self.parked = True

        else:
            # Move the agent following the road if there is no route
            next_position = self.bfs_service.get_main_direction_neighbor(self.pos)
            if  next_position:
                is_outside = next_position[0] < 0 or next_position[1] < 0 or next_position[0] >= 24 or next_position[1] >= 24
                if not is_outside and not any(isinstance(agent, CarAgent) for agent in self.model.grid.get_cell_list_contents([next_position])):
                    self.model.grid.move_agent(self, next_position)
            self.route = self.calculate_route(self.pos, self.end)
