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

def getForbiddenEntrySegments(routes_by_entry_node, segments):
	forbidden_entry_segs = []
	entry_nodes = routes_by_entry_node.keys()

	for seg in segments:
    	fr = points[seg['from']]['area'][0]
    	to = points[seg['to']]['area'][0]
    	if (fr != 'Z' and to == 'Z'): # if seg is from another country to China
        	if (seg['from'] not in entry_nodes) and (seg['to'] not in entry_nodes):
            	forbidden_entry_segs.append(seg)

	return forbidden_entry_segs
