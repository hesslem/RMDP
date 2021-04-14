import help_functions as hp
import math
from order import Order


class Driver:

    DRIVER_SPEED = 1

    def __init__(self, location):
        self.location = location
        self.tour = []
        self.next_stop_projected_time = -1
    
    def update_tour(self, time):
        if len(self.tour) > 0:

            if (self.next_stop_projected_time < 0):
                next_stop_location = self.tour[0].location
                next_stop_distance = hp.manhattan_distance(self.location, next_stop_location)
                self.next_stop_projected_time = time + (next_stop_distance / self.DRIVER_SPEED)

            elif self.next_stop_projected_time <= time:
                self.location = self.tour[0].location

                if isinstance(self.tour[0], Order):
                    self.tour[0].delivery_time = time
                self.tour.pop(0)

                if len(self.tour) > 0:
                    next_stop_location = self.tour[0].location
                    next_stop_distance = hp.manhattan_distance(self.location, next_stop_location)
                    self.next_stop_projected_time = time + (next_stop_distance / self.DRIVER_SPEED)
                else:
                    self.next_stop_projected_time = -1

    def update_location(self, time):

        # only update tour if there is a next stop
        if len(self.tour) > 0:

            next_location = self.tour[0].location
            next_stop_distance = hp.manhattan_distance(next_location, self.location)

            # if driver cannot reach next stop with given speed
            if next_stop_distance > self.DRIVER_SPEED:

                next_stop_x = next_location[0]
                next_stop_y = next_location[1]
                location_x = self.location[0]
                location_y = self.location[1]

                slope = abs(location_y - next_stop_y) / abs(location_x - location_y)
                delta_x = (1 / (1 + slope)) * self.DRIVER_SPEED
                delta_y = slope * delta_x
                location_new_x = (
                    location_x + math.copysign(1, (next_stop_x - location_x)) * delta_x
                )
                location_new_y = (
                    location_y + math.copysign(1, (next_stop_y - location_y)) * delta_y
                )

                self.location = [location_new_x, location_new_y]

            # if driver can reach next stop remove node from tour
            else:
                # if it is an order set delivery time
                if isinstance(self.tour[0], Order):
                    self.tour[0].delivery_time = time
                self.tour.pop(0)

                # if there is a stop after next stop calculate new location
                if len(self.tour) > 0:

                    residual_distance = self.DRIVER_SPEED - next_stop_distance
                    next_stop_x = self.tour[0].location[0]
                    next_stop_y = self.tour[0].location[1]
                    location_x = self.location[0]
                    location_y = self.location[1]

                    slope = abs(location_y - next_stop_y) / abs(location_x - location_y)
                    delta_x = (1 / (1 + slope)) * residual_distance
                    delta_y = slope * delta_x
                    location_new_x = (
                        location_x
                        + math.copysign(1, (next_stop_x - location_x)) * delta_x
                    )
                    location_new_y = (
                        location_y
                        + math.copysign(1, (next_stop_y - location_y)) * delta_y
                    )

                    self.location = [location_new_x, location_new_y]

                # else wait at visited node
                else:
                    self.location = next_location
