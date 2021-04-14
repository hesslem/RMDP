def cheapest_insertion():

    return None


def manhattan_distance(x, y) -> float:

    return sum(abs(a - b) for a, b in zip(x, y))


def calculate_distance_with_location(tour, driver) -> float:
    tour_locations = []
    for node in tour:
        tour_locations.append(node.location)

    tour_locations.insert(0, driver.location)

    distance = 0
    for pair in list(zip(tour_locations, tour_locations[1:])):
        distance = distance + (manhattan_distance(pair[0], pair[1]))

    return distance

def calculate_distance(tour) -> float:
    tour_locations = []
    for node in tour:
        tour_locations.append(node.location)

    distance = 0
    for pair in list(zip(tour_locations, tour_locations[1:])):
        distance = distance + (manhattan_distance(pair[0], pair[1]))

    return distance
