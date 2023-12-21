import heapq
import os
import json
import pandas as pd


class PathFinder:

    TIME_TABLE_PATH = os.path.join(os.path.dirname(__file__), "data/timetables.csv")
    GRAPH_PATH = os.path.join(os.path.dirname(__file__), "data/graph.json")

    @staticmethod
    def check_data_exists() -> dict:
        if not os.path.exists(PathFinder.TIME_TABLE_PATH):
            raise FileNotFoundError("timetables.csv is missing")

        if not os.path.exists(PathFinder.GRAPH_PATH):
            PathFinder.generate_graph()

    @staticmethod
    def generate_graph() -> None:
        # Load the timetable csv
        df = pd.read_csv(PathFinder.TIME_TABLE_PATH, sep="\t", encoding="utf-8")

        # Create two new columns "gare_a" and "gare_b"
        cols = ["gare_a", "gare_b"]
        for col in cols:
            df[col] = ""

        # Split the "trajet" column into two columns "gare_a" and "gare_b"
        for index, row in df.iterrows():
            sp = row["trajet"].split(" - ")
            if len(sp) > 2:
                sp = [sp[0], sp[-1]]
            df.at[index, "gare_a"] = sp[0]
            df.at[index, "gare_b"] = sp[1]

        # Remove "Gare de " from the station names
        for col in cols:
            df[col] = df[col].str.replace("Gare de ", "")

        # Build the graph
        graph = {}

        for index, row in df.iterrows():
            # We add the stations to the graph if they are not already in it and add a key for the other station
            # with the duration as value
            if row["gare_a"] not in graph:
                graph[row["gare_a"]] = {}
            graph[row["gare_a"]][row["gare_b"]] = row["duree"]

            if row["gare_b"] not in graph:
                graph[row["gare_b"]] = {}
            graph[row["gare_b"]][row["gare_a"]] = row["duree"]

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
                return {
                    "path": path,
                    "duration_between_stations": duration_between_stations,
                    "total_duration": distances[end]
                }

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

        # If no path is found, return None
        return None

    @staticmethod
    def minutes_to_hours(minutes: int) -> str:
        return f"{minutes // 60}h{minutes % 60}"

    @staticmethod
    def get_shortest_path(trip: list) -> str:
        try:
            PathFinder.check_data_exists()

            # We want to send trip order by pair
            # ex: ["Nantes", "Lyon", "Paris"] -> [["Nantes", "Lyon"], ["Lyon", "Paris"]]
            trip_order = [trip[i:i + 2] for i in range(len(trip) - 1)]

            result = {}
            for i, step in enumerate(trip_order):
                result[f"{step[0]} - {step[1]}"] = PathFinder.compute_shortest_path(PathFinder.get_graph(), step[0], step[1])

            for k, v in result.items():
                # Fill the header with "#" on both sides until 148 characters + 2 spaces
                print("#" * ((148 - len(k)) // 2) + f" {k} " + "#" * ((148 - len(k)) // 2))

                final_string = ""
                for i, station in enumerate(v["path"]):
                    if i == 0:
                        final_string += station
                    else:
                        final_string += f" -> {PathFinder.minutes_to_hours(v['duration_between_stations'][i])} -> {station}"
                print(final_string)
                print(f"Total duration: {PathFinder.minutes_to_hours(v['total_duration'])}")
                print("#" * 150 + "\n")

            return result
        except Exception as e:
            print(e)
            return str(e)