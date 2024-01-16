from .path_finder import PathFinder


def format_detailed_path(state: str, steps: list = None) -> dict:
    result = {"state": state}
    if steps and state == "CORRECT":
        result["steps"] = steps
    return result


def process_pathfinder(sentences) -> str:
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


def process_pathfinder_detailed(sentence: str) -> dict:
    sentence_split = sentence.split(',')
    if len(sentence_split) > 1:
        if sentence_split[1] not in ["NOT_TRIP", "NOT_FRENCH", "UNKNOWN"]:
            trip_order = sentence_split[1:]
            return format_detailed_path("CORRECT", PathFinder.get_shortest_path(trip_order))
        return format_detailed_path(sentence_split[1])
    return format_detailed_path("UNKNOWN")

