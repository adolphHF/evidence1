from itertools import repeat, chain, product
import random

class BFSService():

    def __init__(self, model, car_class):
        self.model = model
        self.car_class = car_class
        self.road_sections = [
            # Cols
            {
                #SectId: 0
                "cells": list(chain(zip(range(0, 24), repeat(0, 24)), zip(range(0, 24), repeat(1, 24)))),
                "main_direction": "d",
                "secondary_direction": "lr"
            },
            {
                #SectId: 1
                "cells": list(chain(zip(range(0, 14), repeat(6, 14)), zip(range(0, 14), repeat(7, 14)))),
                "main_direction": "u",
                "secondary_direction": "lr"
            },
            {
                #SectId: 2
                "cells": list(chain(zip(range(14, 24), repeat(6, 10)), zip(range(14, 24), repeat(7, 10)))),
                "main_direction": "d",
                "secondary_direction": "lr"
            },
            {
                #SectId: 3
                "cells": list(zip(range(0, 12), repeat(12, 12))),
                "main_direction": "d",
                "secondary_direction": "lr"
            },
            {
                #SectId: 4
                "cells": list(zip(range(0, 12), repeat(13, 12))),
                "main_direction": "d",
                "secondary_direction": "l"
            },
            {
                #SectId: 5
                "cells": list(zip(range(0, 12), repeat(14, 12))),
                "main_direction": "u",
                "secondary_direction": "r"
            },
            {
                #SectId: 6
                "cells": list(zip(range(0, 12), repeat(15, 12))),
                "main_direction": "u",
                "secondary_direction": "lr"
            },
            {
                #SectId: 7
                "cells": list(zip(range(16, 24), repeat(12, 8))),
                "main_direction": "d",
                "secondary_direction": "lr"
            },
            {
                #SectId: 8
                "cells": list(zip(range(16, 24), repeat(13, 8))),
                "main_direction": "d",
                "secondary_direction": "l"
            },
            {
                #SectId: 9
                "cells": list(zip(range(16, 24), repeat(14, 8))),
                "main_direction": "u",
                "secondary_direction": "r"
            },
            {
                #SectId: 10
                "cells": list(zip(range(16, 24), repeat(15, 8))),
                "main_direction": "u",
                "secondary_direction": "lr"
            },
            {
                #SectId: 11
                "cells": list(chain(zip(range(16, 24), repeat(18, 8)), zip(range(16, 24), repeat(19, 8)))),
                "main_direction": "u",
                "secondary_direction": "lr"
            },
            {
                #SectId: 12
                "cells": list(chain(zip(range(0, 24), repeat(22, 24)), zip(range(0, 24), repeat(23, 24)))),
                "main_direction": "u",
                "secondary_direction": "lr"
            },

            # Rows
            {
                #SectId: 13
                "cells": list(chain(zip(repeat(0, 24), range(0, 24)), zip(repeat(1, 24), range(0, 24)))),
                "main_direction": "l",
                "secondary_direction": "ud"
            },
            {
                #SectId: 14
                "cells": list(chain(zip(repeat(5, 8), range(6, 14)), zip(repeat(6, 8), range(6, 14)))),
                "main_direction": "l",
                "secondary_direction": "ud"
            },
            {
                #SectId: 15
                "cells": list(chain(zip(repeat(6, 9), range(15, 24)), zip(repeat(7, 9), range(15, 24)))),
                "main_direction": "l",
                "secondary_direction": "ud"
            },
            {
                #SectId: 16
                "cells": list((zip(repeat(12, 12), range(0, 12)))),
                "main_direction": "l",
                "secondary_direction": "ud"
            },
            {
                #SectId:17
                "cells": list((zip(repeat(13, 12), range(0, 12)))),
                "main_direction": "l",
                "secondary_direction": "u"
            },
            {
                #SectId: 18
                "cells": list(zip(repeat(12, 8), range(16, 24))),
                "main_direction": "l",
                "secondary_direction": "ud"
            },
            {
                #SectId: 19
                "cells": list(zip(repeat(13, 8), range(16, 24))),
                "main_direction": "l",
                "secondary_direction": "u"
            },
            {
                #SectId: 20
                "cells": list(zip(repeat(14, 12), range(0, 12))),
                "main_direction": "r",
                "secondary_direction": "d"
            },
            {
                #SectId: 21
                "cells": list(zip(repeat(15, 12), range(0, 12))),
                "main_direction": "r",
                "secondary_direction": "ud"
            },
            {
                #SectId: 22
                "cells": list((zip(repeat(14, 8), range(16, 24)))),
                "main_direction": "r",
                "secondary_direction": "d"
            },
            {
                #SectId: 23
                "cells": list((zip(repeat(15, 8), range(16, 24)))),
                "main_direction": "r",
                "secondary_direction": "ud"
            },
            {
                #SectId: 24
                "cells": list(chain(zip(repeat(18, 6), range(0, 6)), zip(repeat(19, 6), range(0, 6)))),
                "main_direction": "l",
                "secondary_direction": "ud"
            },
            {
                #SectId: 25
                "cells": list(chain(zip(repeat(18, 5), range(8, 13)), zip(repeat(19, 5), range(8, 13)))),
                "main_direction": "r",
                "secondary_direction": "ud"
            },
            {
                #SectId: 26
                "cells": list(chain(zip(repeat(22, 24), range(0, 24)), zip(repeat(23, 24), range(0, 24)))),
                "main_direction": "r",
                "secondary_direction": "ud"
            },

            # Roundabout
            {
                #SectId: 27
                #upleft corner
                "cells": [(12, 12), (12, 13), (13, 12)],
                "main_direction": "l",
                "secondary_direction": "d"
            },
            {
                #SectId: 28
                #downleft corner
                "cells": [(14, 12), (15, 12), (15, 13)],
                "main_direction": "d",
                "secondary_direction": "r"
            },
            {
                #SectId: 29
                #downright corner
                "cells": [(15, 14), (15, 15), (14, 15)],
                "main_direction": "u",
                "secondary_direction": "r"
            },
            {
                #SectId: 30
                #upright corner
                "cells": [(12, 14), (12, 15), (13, 15)],
                "main_direction": "u",
                "secondary_direction": "l"
            },

            # Parking spots UP
            {
                #SectId: 31
                "cells": [(2,3), (2,17), (8,20), (16,10), (20,4)],
                "main_direction": "u",
                "secondary_direction": "u"
            },

            # Parking spots DOWN
            {
                #SectId: 32
                "cells": [(4,10), (5,20), (11,4), (11,10), (17,3), (21,9)],
                "main_direction": "d",
                "secondary_direction": "d"
            },

            # Parking spots LEFT
            {
                #SectId: 33
                "cells": [(9,2), (8,8), (19,20)],
                "main_direction": "l",
                "secondary_direction": "l"
            },

            # Parking spots RIGHT
            {
                #SectId: 34
                "cells": [(6,5), (17,17), (19, 17)],
                "main_direction": "r",
                "secondary_direction": "r"
            },

        ]
        self.building_cells = list(chain( 
            product(range(2, 12), range(2, 6)),
            product(range(2, 5), range(8, 12)),
            product(range(7, 12), range(8, 12)),

            product(range(16, 18), range(2, 6)),
            product(range(16, 18), range(8, 12)),
            product(range(20, 22), range(2, 6)),
            product(range(20, 22), range(8, 12)),

            product(range(2, 6), range(16, 22)),
            product(range(8, 12), range(16, 22)),

            product(range(16, 22), range(16, 18)),
            product(range(16, 22), range(20, 22)),

            product(range(13, 15), range(13, 15)),
        ))
        self.parking_cells = [
            (9, 2),
            (2, 3),
            (17, 3),
            (11, 4),
            (20, 4),#5
            (6, 5),
            (8, 8),
            (21, 9),
            (4, 10),
            (11, 10),#10
            (16, 10),
            (2, 17),
            (17, 17),
            (19, 17),
            (5, 20), #15
            (8, 20),
            (19, 20)
        ]

    def get_main_direction_neighbor(self, position):
        # Find the road section that contains the current position
        road_sections_containing_position = []
        for road_section in self.road_sections:
            if position in road_section['cells']:
                road_sections_containing_position.append(road_section)
        
        # If only one section, return the main direction
        if len(road_sections_containing_position) == 1:
            road_section = road_sections_containing_position[0]
            main_direction = road_section['main_direction']
        # Select one of the two main directions randomly
        else:
            road_section_1, road_section_2 = road_sections_containing_position
            main_direction_1 = road_section_1['main_direction']
            main_direction_2 = road_section_2['main_direction']
            main_direction = main_direction_1 if random.random() < 0.5 else main_direction_2
        
        x, y = position
        if main_direction == 'u':
            position = (x-1, y)
        if main_direction == 'd':
            position = (x+1, y)
        if main_direction == 'l':
            position = (x, y-1)
        if main_direction == 'r':
            position = (x, y+1)
    
        if position not in self.building_cells and position not in self.parking_cells:
            return position
        return None
            
    def get_neighbors(self, position):
        # Find the road sections that contain the current position
        road_sections_containing_position = []
        for road_section in self.road_sections:
            if position in road_section['cells']:
                road_sections_containing_position.append(road_section)
        
        # If only one section, both main direction and secondary direction are valid
        if len(road_sections_containing_position) == 1:
            road_section = road_sections_containing_position[0]

            main_direction = road_section['main_direction']
            secondary_direction = road_section['secondary_direction']
            valid_directions = main_direction + secondary_direction

        # If two sections, only the main directions of each sections are valid
        else:
            road_section_1, road_section_2 = road_sections_containing_position
            main_direction_1 = road_section_1['main_direction']
            main_direction_2 = road_section_2['main_direction']
            valid_directions = main_direction_1 + main_direction_2

        x, y = position
        neighbors = []
        if 'u' in valid_directions:
            neighbors.append((x-1, y))
        if 'd' in valid_directions:
            neighbors.append((x+1, y))
        if 'l' in valid_directions:
            neighbors.append((x, y-1))
        if 'r' in valid_directions:
            neighbors.append((x, y+1))
        return neighbors

    def bfs(self, start, end):
        queue = [start]
        visited = set()
        predecessors = {}

        while queue:
            current = queue.pop(0)
            if current == end:
                return predecessors

            for neighbor in self.get_neighbors(current):
                is_empty_cell = neighbor not in self.building_cells or neighbor == end
                is_out_of_bounds = neighbor[0] < 0 or neighbor[0] >= 24 or neighbor[1] < 0 or neighbor[1] >= 24
                if not is_out_of_bounds:
                    cellmates = self.model.grid.get_cell_list_contents([neighbor])
                    is_empty_cell = (neighbor == end) or (is_empty_cell and not any(isinstance(agent, self.car_class) for agent in cellmates))

                if neighbor not in visited and is_empty_cell and not is_out_of_bounds:
                    visited.add(neighbor)
                    predecessors[neighbor] = current
                    queue.append(neighbor)
        
        return predecessors


    def get_path(self, predecessors, start, end):
        current = end
        path = []
        while current != start:
            path.append(current)
            if current not in predecessors:
                return None # No path found
            current = predecessors[current]
        path.append(start)
        path.reverse()
        return path

    def get_route(self, start, end):
        predecessors = self.bfs(start, end)
        path = self.get_path(predecessors, start, end)
        return path
