import heapq
import logging
import os
import json
import pandas as pd


class PathFinder:

    TIME_TABLE_PATH = os.path.join(os.path.dirname(__file__), "data/timetables_formatted.csv")
    GRAPH_PATH = os.path.join(os.path.dirname(__file__), "data/graph.json")

    @staticmethod
    def check_data_exists() -> None:
        if not os.path.exists(PathFinder.TIME_TABLE_PATH):
            raise FileNotFoundError("timetables_formatted.csv is missing")

        if not os.path.exists(PathFinder.GRAPH_PATH):
            PathFinder.generate_graph()

    @staticmethod
    def generate_graph() -> None:
        # Load the timetable csv
        df = pd.read_csv(PathFinder.TIME_TABLE_PATH, sep="\t", encoding="utf-8")

        # Build the graph
        graph = {}

        for index, row in df.iterrows():
            # We add the stations to the graph if they are not already in it and add a key for the other station
            # with the duration as value
            if row["gare_a_city"] not in graph:
                graph[row["gare_a_city"]] = {}
            graph[row["gare_a_city"]][row["gare_b_city"]] = row["duree"]

            if row["gare_b_city"] not in graph:
                graph[row["gare_b_city"]] = {}
            graph[row["gare_b_city"]][row["gare_a_city"]] = row["duree"]

        try:
            # Save the graph
            with open(PathFinder.GRAPH_PATH, "w") as f:
                json.dump(graph, f, indent=4)
        except IOError:
            raise IOError("Unable to write the graph to file")

    @staticmethod
    def get_graph() -> dict:
        with open(PathFinder.GRAPH_PATH, "r") as f:
            graph = json.load(f)

        return graph

    @staticmethod
    def generate_response_dict(path: list = None, duration_between_stations: list = None, total_duration: int = 0) -> dict:
        print(path)
        response_dict = {
            "path": path if path else [],
            "duration_between_stations": duration_between_stations if duration_between_stations else [],
            "total_duration": total_duration
        }
        return response_dict

    @staticmethod
    def compute_shortest_path(graph: dict, start: str, end: str) -> dict | None:
        # Set the distance to all stations to infinity
        distances = {station: float('inf') for station in graph}

        # Distance from the start to itself is 0
        distances[start] = 0

        # We set the priority queue with the start station
        priority_queue = [(0, start)]

        # Create a dictionary to store the previous station in the path
        previous_station = {station: None for station in graph}

        while priority_queue:
            # Pop the station with the shortest distance from the heap, so we consider it first
            current_distance, current_station = heapq.heappop(priority_queue)

            # If the current station is the destination, return the shortest distance
            if current_station == end:
                path = []
                duration_between_stations = [None]
                while current_station is not None:
                    path.append(current_station)
                    previous = previous_station[current_station]
                    if previous:
                        duration_between_stations.append(graph[current_station][previous])
                    current_station = previous_station[current_station]
                path.reverse()
                duration_between_stations.reverse()
                return PathFinder.generate_response_dict(path, duration_between_stations, distances[end])

            # Skip if the current station is already visited
            if current_distance > distances[current_station]:
                continue

            # Explore neighbors
            for neighbor, weight in graph[current_station].items():
                distance = current_distance + weight

                # If a shorter path is found, update the distance and add to the priority queue
                if distance < distances[neighbor]:
                    # The fastest way to reach the neighbor is from the current station, so we just assign
                    # the distance to the current_station + the weight of the edge between the current station
                    # and the neighbor to the neighbor
                    distances[neighbor] = distance
                    previous_station[neighbor] = current_station
                    # We add the neighbor to the priority queue with the distance as priority
                    # It means that the neighbor will be explored before the other stations if the distance is shorter
                    # than the other stations
                    # ex: if the distance from the start to the neighbor is 10 and the distance from the start to
                    # the other station is 20, the neighbor's neighbors will be explored before the other station
                    heapq.heappush(priority_queue, (distance, neighbor))

        # If no path is found, return empty dict
        return PathFinder.generate_response_dict(["UNKNOWN"])

    @staticmethod
    def minutes_to_hours(minutes: int) -> str:
        hours = str(minutes // 60).zfill(2)
        test = str(minutes % 60).zfill(2)
        return f"{hours}h{test}"

    @staticmethod
    def get_shortest_path(trip: list) -> list:
        results = []

        try:
            PathFinder.check_data_exists()

            # Uppercase each word in the trip
            trip = [station.upper() for station in trip]

            # We want to send trip order by pair
            # ex: ["Nantes", "Lyon", "Paris"] -> [["Nantes", "Lyon"], ["Lyon", "Paris"]]
            trip_order = [trip[i:i + 2] for i in range(len(trip) - 1)]

            if len(trip_order) == 0:
                return [PathFinder.generate_response_dict(["UNKNOWN"])]

            for i, step in enumerate(trip_order):
                results.append(PathFinder.compute_shortest_path(PathFinder.get_graph(), step[0], step[1]))

            return results
        except Exception as e:
            logging.error(f"{e} not found in the graph")
            return results + [PathFinder.generate_response_dict(["UNKNOWN"])]
