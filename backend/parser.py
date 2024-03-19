import json
import random
import re
from geopy.distance import geodesic

class TravelPlanner:
    def __init__(self, max_duration, max_cost):
        self.dataset_file =  "./backend/dataset.json"
        self.max_duration = max_duration
        self.max_cost = max_cost
        self.average_speed = 60
        self.places = []

    def load_dataset(self):
        with open(self.dataset_file, "r") as json_file:
            self.places = json.load(json_file)

    def estimate_travel_time(self, distance):
        return distance / self.average_speed

    def find_random_next_place(self, current_place, unvisited_places):
        return random.choice(unvisited_places)

    def plan_travel_path(self, duration_tolerance=0, cost_tolerance=0):
        self.load_dataset()

        # Sort places by category and then by cost in ascending order
        sorted_places = sorted(self.places, key=lambda x: (x['categoryName'] not in ['Restaurant', 'Bar'], x['price']))

        max_places = []
        total_duration = 0
        total_cost = 0

        # Define regex patterns for restaurant and bar categories
        restaurant_pattern = re.compile(r'restaurant|diner|eatery', re.IGNORECASE)
        bar_pattern = re.compile(r'bar|pub|nightclub', re.IGNORECASE)

        # First, prioritize filling the budget constraint with a mix of places including restaurants and bars
        for place in sorted_places:
            if total_cost + place['price'] <= self.max_cost + cost_tolerance and total_duration < self.max_duration:
                # Calculate the estimated travel time to the current place
                if max_places:
                    distance_to_place = geodesic((max_places[-1]['location']['lat'], max_places[-1]['location']['lng']), 
                                                (place['location']['lat'], place['location']['lng'])).kilometers
                    travel_time = self.estimate_travel_time(distance_to_place)
                else:
                    travel_time = 0
                
                # Add the place if the cost constraint allows
                if total_duration + travel_time + place['time'] <= self.max_duration:
                    max_places.append(place)
                    total_cost += place['price']
                    total_duration += travel_time + place['time']
                elif restaurant_pattern.search(place['categoryName']) or bar_pattern.search(place['categoryName']):
                    # If the place is a restaurant or bar, allow exceeding the duration constraint
                    max_places.append(place)
                    total_cost += place['price']
                    total_duration += travel_time + place['time']

        # Initialize variables
        unvisited_places = max_places.copy()
        random.shuffle(unvisited_places)  # Shuffle the list of unvisited places

        current_place = unvisited_places.pop(0)  # Randomly select the initial place
        path = [(current_place, 0)]  # Path with distance from one location to the next

        # Find the next place to visit randomly
        while unvisited_places:
            next_place = self.find_random_next_place(current_place, unvisited_places)
            distance = geodesic((current_place['location']['lat'], current_place['location']['lng']), 
                                (next_place['location']['lat'], next_place['location']['lng'])).kilometers
            travel_time = self.estimate_travel_time(distance)
            path.append((next_place, travel_time))
            unvisited_places.remove(next_place)
            current_place = next_place

        # Print the path of maximized places by the shortest distance
        total_distance = sum(distance for _, distance in path[1:])
        for i in path:
            i[0].pop("location")
        return path, total_duration, total_cost, total_distance
    