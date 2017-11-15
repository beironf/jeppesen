
possible_routes = []

def isForbidden(seg, forbidden_segs, forbidden_entry_segs):
	if seg in forbidden_segs:
		return True
	elif seg in forbidden_entry_segs:
		return True
	else:
		return False

def getSegment(fr, to, segments):
	seg = [seg for seg in segments if (seg['from']==fr and seg['to']==to)]
	return seg

def find_path(seg, used_segs, points, entry_nodes):
	node = seg['to']
	for to in possible_destinations[node]:
		seg = getSegment(node, to, segments)
		if isForbidden(seg, forbidden_segs, forbidden_entry_segs):
			if (to in entry_nodes or points[to]['area'][0]!='Z'):
				possible_routes.append([used_segs, seg])
		else:
			find_path(seg, [used_segs, seg], points, entry_nodes)


def getAllowedRoutes(forbidden_segs, forbidden_entry_segs, segments, points, possible_destinations, entry_nodes):
	start_segs = []

	for seg in segments:
    	fr = points[seg['from']]['area'][0]
    	to = points[seg['to']]['area'][0]
    	if (fr != 'Z' and to == 'Z'): # if seg is from another country to China
        	start_segs.append(seg)

	for start_seg in start_segs:
		used_segs = []
		find_path(start_seg, used_segs, points, entry_nodes)

	return possible_routes