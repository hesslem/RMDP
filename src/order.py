class Order:
    def __init__(self, time, location, restaurant):
        self.time = time
        self.location = location
        self.restaurant = restaurant
        self.delivery_time = None
        self.served = False

    def __str__(self):
        return str([self.time, self.location, self.restaurant])
