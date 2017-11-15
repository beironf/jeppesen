#Program to create forbid segments
#The program checks all mandatory routes, grouped by entry point to China, and 
#finds the set of segments that need to be forbidden so that only the mandatory
#routes are possible to choose. 

import parse_data

segments = parse_data.getSegments()
possible_destinations = parse_data.getPossibleDestinations(segments)
allowed_routes = parse_data.getAllowedRoutes()
points = parse_data.getPoints(segments)
routes_by_entry_node = parse_data.getRoutesForAllEntryNodes(allowed_routes)

forbidden_segs = {}

for entry_node in routes_by_entry_node:
    forbidden_tmp = []
    current_routes = routes_by_entry_node[entry_node]
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
                if (sg not in used_segs) and (sg not in forbidden_tmp):
                        forbidden_tmp.append(sg)
    forbidden_segs[entry_node] = forbidden_tmp

#print(possible_segs)
#print(used_segs)
#print(forbidden_tmp)
#print(forbidden_segs['WPT INTIK'])
