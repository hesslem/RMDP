import numpy as np
import matplotlib.pyplot as plt
from driver import Driver
from restaurant import Restaurant
from order import Order
import help_functions as hp
import itertools

# initialize parameters in t=0

# order horizon
T_MAX = 420

# service area
service_area = ([0, 0], [100, 100])

# number of drivers
NUM_DRIVERS = 20
# driver speed
Driver.DRIVER_SPEED = 10

drivers = []
# create drivers
for i in range(NUM_DRIVERS):
    # todo: where do drivers start
    # i.e. random, center, etc.
    # pass location in constructor
    driver_x = np.random.uniform(service_area[0][0], service_area[1][0])
    driver_y = np.random.uniform(service_area[0][1], service_area[1][1])
    drivers.append(Driver([driver_x, driver_y]))
# make list of drivers immutable
drivers = tuple(drivers)
print('### DRIVERS ###')
for driver in drivers:
    print(driver.location)
print('###############')

# location of restaurants
NUM_RESTAURANTS = 110
restaurants = []
for i in range(NUM_RESTAURANTS):
    restaurant_x = np.random.uniform(service_area[0][0], service_area[1][0])
    restaurant_y = np.random.uniform(service_area[0][1], service_area[1][1])
    restaurants.append(Restaurant([restaurant_x, restaurant_y]))
# make list of restaurants immutable
restaurants = tuple(restaurants)

# todo: create delivery zones

# poisson point process for orders
order_times = np.random.poisson(lam=1, size=T_MAX)

order_list = []
unserved = []
total_time = 0

for time in itertools.count(start=1):

    # assign orders in the order horizon
    if time <= T_MAX:
        num_orders = order_times[time-1]
        print('Number of orders in time {} : {}'.format(time, num_orders))
        if num_orders > 0:
            new_orders = []
            for order in range(num_orders):
                order_x = np.random.uniform(service_area[0][0], service_area[1][0])
                order_y = np.random.uniform(service_area[0][1], service_area[1][1])
                order_restaurant = np.random.randint(NUM_RESTAURANTS)
                new_order = Order(time, [order_x, order_y], order_restaurant)
                new_orders.append(new_order)
                order_list.append(new_order)
                unserved.append(new_order)

            # determine cheapest insertion
            # update tour of driver with fastest delivery time
            # iterate over new orders
            for order in new_orders:
                print('Order: {}'.format(order))
                fastest_time = np.inf
                fastest_driver = None
                fastest_tour_driver = []

                # assign order to driver
                for driver_num, driver in enumerate(drivers):
                    fastest_new_time_driver = np.inf
                    fastest_new_tour_driver = []
                    if len(driver.tour) > 0:
                        for i in range(1, len(driver.tour) + 1):
                            new_tour = driver.tour.copy()
                            # insert restaurant and order in existing tour
                            new_tour.insert(i, restaurants[order.restaurant])
                            new_tour.insert(i+1, order)
                            new_tour_time = hp.calculate_time(new_tour, driver)
                            if new_tour_time < fastest_new_time_driver:
                                fastest_new_time_driver = new_tour_time
                                fastest_new_tour_driver = new_tour.copy()

                    else:
                        restaurant_order_pair = [restaurants[order.restaurant], order]
                        new_tour_time = hp.calculate_time(restaurant_order_pair, driver)
                        fastest_new_time_driver = new_tour_time
                        fastest_new_tour_driver = restaurant_order_pair

                    if fastest_new_time_driver < fastest_time:
                        fastest_time = fastest_new_time_driver
                        fastest_tour_driver = fastest_new_tour_driver.copy()
                        fastest_driver = driver_num

                print('Fastest driver: {}'.format(fastest_driver))
                drivers[fastest_driver].tour = fastest_tour_driver.copy()

    # update position of all drivers
    for number, driver in enumerate(drivers):
        driver.update_location(time)
        print('Diver #{} status:'.format(number))
        print('Location: {}'.format(driver.location))
        print('Tour: {}'.format([x.location for x in driver.tour]))
    
    # remove served customers from unserved list
    for order in unserved:
        if order.delivery_time > 0:
            unserved.remove(order)
    
    # quit loop if all customers have been served
    if not unserved:
        total_time = time
        break


print('### RESULTS ###')
print('Total time needed until all customers have been served: {}'.format(total_time))
print('Total number of orders: {}'.format(len(order_list)))
served = 0
total_delay = 0
for order in order_list:
    total_delay = total_delay + order.delay
print('Total delay: {}'.format(total_delay))