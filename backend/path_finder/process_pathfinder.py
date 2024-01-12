from .path_finder import PathFinder


def process_pathfinder(sentences):
    results = []

    for sentence in sentences:
        sentence_split = sentence.split(',')
        if len(sentence_split) > 1:
            if sentence_split[1] not in ["NOT_TRIP", "NOT_FRENCH", "UNKNOWN"]:
                trip_order = sentence_split[1:]
                pathfinder_result = PathFinder.get_shortest_path(trip_order)
                for res in pathfinder_result:
                    results.append(f"{sentence_split[0]},{','.join(res['path'])}")
            else:
                results.append(sentence)
        else:
            results.append(f"{sentence_split[0]},UNKNOWN")

    return '\n'.join(results)

