#Program to create forbid segments
#The program checks all mandatory routes, grouped by entry point to China, and 
#finds the set of segments that need to be forbidden so that only the mandatory
#routes are possible to choose. 

def getForbiddenSegments(routes_by_entry_node, segments):
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
    
    return forbidden_segs

def getForbiddenSegments2(routes_by_entry_node, segments, allowed_routes):
    forbidden_segs = {}

    for entry_node in routes_by_entry_node:
        current_routes = routes_by_entry_node[entry_node]

        #Find all used segments
        used_segs = []
        for route in current_routes:
            for seg in route:
                if seg not in used_segs:
                    used_segs.append(seg)

        #Find all possible segments
        possible_segs = []
        for used_seg in used_segs:
            for possible_seg in segments:
                if possible_seg['from'] == used_seg['from']:
                    possible_segs.append(possible_seg)

        #Find which segments to forbid
        forbidden_tmp = []
        for seg in possible_segs:
            if (seg not in used_segs) and (seg not in forbidden_tmp):
                forbidden_tmp.append(seg)
        forbidden_segs[entry_node] = forbidden_tmp

    return forbidden_segs

def getForbiddenEntrySegments(routes_by_entry_node, entry_nodes, segments, points):
    forbidden_entry_segs = []

    for seg in segments:
        fr = points[seg['from']]['area'][0]
        to = points[seg['to']]['area'][0]
        if (fr != 'Z' and to == 'Z'): # if seg is from another country to China
            if (seg['from'] not in entry_nodes) and (seg['to'] not in entry_nodes):
                forbidden_entry_segs.append(seg)

    return forbidden_entry_segs
