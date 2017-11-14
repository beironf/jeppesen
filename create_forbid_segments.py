# Program to create forbid segments

import parse_data

segments = parse_data.getSegments()
possible_destinations = parse_data.getPossibleDestinations(segments)
allowed_routes = parse_data.getAllowedRoutes()
points = parse_data.getPoints(segments)
routes_for_all_entry_nodes = parse_data.getRoutesForAllEntryNodes(allowed_routes)

forbidden_segs = {}

for entry_node in routes_for_all_entry_nodes:
    forbidden_tmp = []
    current_routes = routes_for_all_entry_nodes[entry_node]
    for route in current_routes:
        for seg in route:
            used_segs = []
            for rt in current_routes:
                for sg in rt:
                    if sg['from'] == seg['from'] and not(sg in used_segs):
                        used_segs.append(sg)
            possible_segs = []
            for sg in segments:
                if sg['from'] == seg['from']:
                    possible_segs.append(sg)
            for sg in possible_segs:
                if not(sg in used_segs and sg in forbidden_tmp):
                    forbidden_tmp.append(sg)
    forbidden_segs[entry_node] = forbidden_tmp

print(forbidden_segs['WPT INTIK'])
