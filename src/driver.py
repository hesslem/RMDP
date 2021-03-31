import help_functions as hp
import math
from order import Order


class Driver:
    def __init__(self, location):
        self.location = location
        self.tour = []

    def update_location(self):

        if len(self.tour) > 0:

            next_location = self.tour[0].location
            next_stop_distance = hp.manhattan_distance(next_location, self.location)

            if next_stop_distance > 5:

                next_stop_x = next_location[0]
                next_stop_y = next_location[1]
                location_x = self.location[0]
                location_y = self.location[1]

                slope = abs(location_y - next_stop_y) / abs(location_x - location_y)
                delta_x = (1 / (1 + slope)) * 5
                delta_y = slope * delta_x
                location_new_x = (
                    location_x + math.copysign(1, (next_stop_x - location_x)) * delta_x
                )
                location_new_y = (
                    location_y + math.copysign(1, (next_stop_y - location_y)) * delta_y
                )

                self.location = [location_new_x, location_new_y]

            else:

                if isinstance(self.tour[0], Order):
                    self.tour[0].served = True
                    print('### SERVED ###')
                self.tour.pop(0)

                if len(self.tour) > 0:

                    residual_distance = 5 - next_stop_distance
                    next_stop_x = self.tour[0].location[0]
                    next_stop_y = self.tour[0].location[1]
                    location_x = self.location[0]
                    location_y = self.location[1]

                    slope = abs(location_y - next_stop_y) / abs(location_x - location_y)
                    delta_x = (1 / (1 + slope)) * residual_distance
                    delta_y = slope * delta_x
                    location_new_x = (
                        location_x + math.copysign(1, (next_stop_x - location_x)) * delta_x
                    )
                    location_new_y = (
                        location_y + math.copysign(1, (next_stop_y - location_y)) * delta_y
                    )

                    self.location = [location_new_x, location_new_y]

                else:
                    self.location = next_location
