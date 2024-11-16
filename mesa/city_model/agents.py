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

    def check_semaphore(self):
        print("si esta checando semaforos")
        cellmates = self.model.grid.get_cell_list_contents([self.pos]) #with this, check if any other agent
        if len(cellmates) > 1:  # Check if there are multiple agents in the cell
            for agent in cellmates:
                # Check if the agent is of type TrafficLightAgent
                if isinstance(agent, TrafficLightAgent):
                    semaphore = agent
                    print(f"Semaphore found at {self.pos}, allow_pass: {semaphore.allow_pass}")
                    return semaphore.allow_pass
                
        else:
            print("no semaphore here")
        return None 

        """
        traffic_light_in_pos = self.model.agents_by_type[TrafficLightAgent].select(lambda a: a.pos == self.pos)
        if len(traffic_light_in_pos) > 0:
            traffic_light = traffic_light_in_pos[0]
            if traffic_light.allow_pass == False:
                print("WAITING")
                return # Espera en rojo
        #Verify the current cell don't have a semaphore and evaluate it's state
        x,y = self.pos
        if self.model.grid.properties["semaphore"].data[x, y] == 1:

            print("A semaphore was reached")
        """
        

    def step(self):
        """Perform one step in the simulation."""
        if self.route:
            # Get the next position in the route
            #if self.check_semaphore():
            val = self.check_semaphore()
            print(val)
            next_position = self.route.pop(0)  # Remove and get the first step
            # Move the agent to the next position
            self.model.grid.move_agent(self, next_position)
            # Update current position
            #self.current_position = next_position#TODO why does it need this?
            print(f"Moved to {next_position}. Remaining route: {self.route}")

        else:
            # Route is empty, the car has reached its destination
            self.parked = True
            print("Car is parked. Route complete.")


