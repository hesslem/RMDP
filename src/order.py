class Order:

    buffer = 40

    def __init__(self, time, location, restaurant):
        self.order_time = time
        self.location = location
        self.restaurant = restaurant
        self.delivery_time = 0

    def __str__(self):

        return str([self.order_time, self.location, self.restaurant])

    @property
    def delay(self):

        return max(0, self.delivery_time - (self.order_time + self.buffer))
