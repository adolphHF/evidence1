import mesa
from mesa import Model
from agents import CarAgent, TrafficLightAgent
from mesa.space import MultiGrid
import numpy as np

class CityModel(mesa.Model):
    """Modelo que representa una ciudad con capas de edificios y estacionamientos en una cuadrícula."""

    def __init__(self, width=24, height=24, num_buildings=11, num_parking=17, seed=None):
        super().__init__(seed=seed)
        self.width = width
        self.height = height
        self.num_buildings = num_buildings
        self.num_parking = num_parking
        self.grid = MultiGrid(width, height, torus=False)


        self.parking_layer = mesa.space.PropertyLayer("parkings", width, height, np.int64(0), np.int64)

        self.roundabout_layer = mesa.space.PropertyLayer("roundabout", width, height, np.int64(0), np.int64)

        self.buildings_layer= mesa.space.PropertyLayer("buildings", width, height, np.int64(0), np.int64)

        self.grid = mesa.space.MultiGrid(width, height, True, property_layers=[self.buildings_layer, self.parking_layer, self.roundabout_layer])

        #Primer bloque
        self.add_building(2, 2, 11, 5)
        self.add_building(16, 2, 17, 5)
        self.add_building(20, 2, 21, 5)
        #estacionamientos primer bloque
        self.add_parking(2, 3, 2, 3)
        self.add_parking(6, 5, 6, 5)
        self.add_parking(9, 2, 9, 2)
        self.add_parking(11, 4,11, 4)
        self.add_parking(17, 3, 17, 3)
        self.add_parking(20, 4, 20, 4)


        #Segundo Bloque
        self.add_building(2, 8, 4, 11)
        self.add_building(7, 8, 11, 11)
        self.add_building(16, 8, 17, 11)
        self.add_building(20, 8, 21, 11)
        #estacionamientos Segundo bloque
        self.add_parking(4, 10, 4, 10)
        self.add_parking(8, 8, 8, 8)
        self.add_parking(11, 10, 11, 10)
        self.add_parking(16, 10, 16, 10)
        self.add_parking(21, 9, 21, 9)


        #Tercer bloque
        self.add_building(2, 16, 5, 21)
        self.add_building(8, 16, 11, 21)
        self.add_building(16, 16, 21, 17)
        self.add_building(16, 20, 21, 21)
        #estacionamientos tercer bloque
        self.add_parking(2, 17, 2, 17)
        self.add_parking(5, 20, 5, 20)
        self.add_parking(8, 20, 8, 20)
        self.add_parking(17, 17, 17, 17)
        self.add_parking(19, 17, 19, 17)
        self.add_parking(19, 20, 19, 20)

        self.add_roundabout(13,13, 14,14)

        self.traffic_light_positions = [(10, 0), (10, 1)]
        self.traffic_lights = []
        for pos in self.traffic_light_positions:
            traffic_light = TrafficLightAgent(model=self)
            self.grid.place_agent(traffic_light, pos)
            self.traffic_lights.append(traffic_light)

        car = CarAgent(self)
        self.grid.place_agent(car, (0,0))

    def add_building(self, x_start, y_start, x_end, y_end):
        """Rellenar la capa de edificios en la cuadrícula dentro de las coordenadas dadas."""
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                self.buildings_layer.set_cell((x,y),1)

    def add_parking(self, x_start, y_start, x_end, y_end):
        """Rellenar la capa de estacionamientos en la cuadrícula dentro de las coordenadas dadas."""
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
               self.parking_layer.set_cell((x,y),1)

    def add_roundabout(self, x_start, y_start, x_end, y_end):
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                self.roundabout_layer.set_cell((x,y),1)


    def step(self):
        """Actualiza el estado de cada semáforo en el modelo."""
        self.agents.do("step")


    def display_combined_grid(self):
        """Mostrar una representación combinada de las capas de edificios, estacionamientos y glorieta."""
        print("Ciudad:")
        for x in range(self.width):
            row_display = ""
            for y in range(self.height):
                if any(isinstance(agent, TrafficLightAgent) for agent in self.grid.get_cell_list_contents((x, y))):
                    traffic_light = next(agent for agent in self.grid.get_cell_list_contents((x, y)) if isinstance(agent, TrafficLightAgent))
                    row_display += f" {traffic_light.color[0].upper()} "
                elif any(isinstance(agent, CarAgent) for agent in self.grid.get_cell_list_contents((x, y))):
                    car = next(agent for agent in self.grid.get_cell_list_contents((x, y)) if isinstance(agent, CarAgent))
                    row_display += " C "
                elif self.roundabout_layer[x][y] == 1:
                    row_display += " A "
                elif self.parking_layer[x][y] == 1:
                    row_display += " P "
                elif self.buildings_layer[x][y] == 1:
                    row_display += " B "
                else:
                    row_display += " . "
            print(row_display)
        print("\n")