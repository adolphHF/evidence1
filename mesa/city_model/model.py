import mesa
from mesa import Model
from mesa.space import MultiGrid

class CityModel(Model):
    """Modelo que representa una ciudad con capas de edificios y estacionamientos en una cuadrícula."""

    def __init__(self, width=24, height=24, num_buildings=11, num_parking=17, seed=None):
        super().__init__(seed=seed)
        self.width = width
        self.height = height
        self.num_buildings = num_buildings
        self.num_parking = num_parking
        self.grid = MultiGrid(width, height, torus=False)

        self.buildings_layer = [[0 for _ in range(width)] for _ in range(height)]

        self.parking_layer = [[0 for _ in range(width)] for _ in range(height)]

        self.roundabout_layer = [[0 for _ in range(width)] for _ in range(height)]


        #Primer bloque
        self.add_building(2, 2, 5, 11)
        self.add_building(2, 16, 5, 17)
        self.add_building(2, 20, 5, 21)
        #estacionamientos primer bloque
        self.add_parking(3, 2, 3, 2)
        self.add_parking(5, 6, 5, 6)
        self.add_parking(2, 9, 2, 9)
        self.add_parking(4, 11, 4, 11)
        self.add_parking(3, 17, 3, 17)
        self.add_parking(4, 20, 4, 20)


        #Segundo Bloque
        self.add_building(8, 2, 11, 4)
        self.add_building(8, 7, 11, 11)
        self.add_building(8, 16, 11, 17)
        self.add_building(8, 20, 11, 21)
        #estacionamientos Segundo bloque
        self.add_parking(10, 4, 10, 4)
        self.add_parking(8, 8, 8, 8)
        self.add_parking(10, 11, 10, 11)
        self.add_parking(10, 16, 10, 16)
        self.add_parking(9, 21, 9, 21)


        #Tercer bloque
        self.add_building(16, 2, 21, 5)
        self.add_building(16, 8, 21, 11)
        self.add_building(16, 16, 17, 21)
        self.add_building(20, 16, 21, 21)
        #estacionamientos tercer bloque
        self.add_parking(17, 2, 17, 2)
        self.add_parking(20, 5, 20, 5)
        self.add_parking(20, 8, 20, 8)
        self.add_parking(17, 17, 17, 17)
        self.add_parking(17, 19, 17, 19)
        self.add_parking(20, 19, 20, 19)

        self.add_roundabout(13,13, 14,14)

        self.traffic_light_positions = [(8, 0), (8, 1)]
        self.traffic_lights = []
        for pos in self.traffic_light_positions:
            traffic_light = TrafficLightAgent(model=self)
            self.grid.place_agent(traffic_light, pos)
            self.traffic_lights.append(traffic_light)

    def add_building(self, x_start, y_start, x_end, y_end):
        """Rellenar la capa de edificios en la cuadrícula dentro de las coordenadas dadas."""
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                self.buildings_layer[y][x] = 1

    def add_parking(self, x_start, y_start, x_end, y_end):
        """Rellenar la capa de estacionamientos en la cuadrícula dentro de las coordenadas dadas."""
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                self.parking_layer[y][x] = 1

    def add_roundabout(self, x_start, y_start, x_end, y_end):
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                self.roundabout_layer[y][x] = 1


    def step(self):
        """Actualiza el estado de cada semáforo en el modelo."""
        for traffic_light in self.traffic_lights:
            traffic_light.step()


    def display_combined_grid(self):
        """Mostrar una representación combinada de las capas de edificios, estacionamientos y glorieta."""
        print("Ciudad:")
        for y in range(self.height):
            row_display = ""
            for x in range(self.width):
                if any(isinstance(agent, TrafficLightAgent) for agent in self.grid.get_cell_list_contents((x, y))):
                    traffic_light = next(agent for agent in self.grid.get_cell_list_contents((x, y)) if isinstance(agent, TrafficLightAgent))
                    row_display += f" {traffic_light.color[0].upper()} "
                elif self.roundabout_layer[y][x] == 1:
                    row_display += " A "
                elif self.parking_layer[y][x] == 1:
                    row_display += " P "
                elif self.buildings_layer[y][x] == 1:
                    row_display += " B "
                else:
                    row_display += " . "
            print(row_display)
        print("\n")