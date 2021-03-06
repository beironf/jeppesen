#Program to create forbid segments and sequences
#The program checks all mandatory routes, grouped by entry point to China, and 
#finds the set of segments and sequences that need to be forbidden so that only the mandatory
#routes are possible to choose. 

def getAllowedSegmentsFrom(fr, allowed_segments):
        segs = [seg for seg in allowed_segments if seg['from']==fr]
        return segs

def getAllowedSegmentsFromEntryNode(entry_node, routes_by_entry_node):
        segs = []
        for route in routes_by_entry_node[entry_node]:
            segs.extend([sg for sg in route])
        return segs

def issubset(a, b):
    if len(a)>len(b):
        return False
    else:
        if len(a)==1:
            a = [a]
        return all([any([a[i]==b[j] for j in range(len(b))]) for i in range(len(a))])

def getUsedSegsBeforeNode(node, route):
    used_segs = []
    for sg in route:
        if sg['to'] == node:
            used_segs.append(sg)
            return used_segs
        else:
            used_segs.append(sg)
    return used_segs

def getUniqueElements(l):
    unique = []
    [unique.append(x) for x in l if x not in unique]
    return unique

def find_forbidden_seq(seg, used_segs, allowed_segments, routes_by_entry_node):
    node = seg['to']
    next_allowed_segs = getAllowedSegmentsFrom(node, getAllowedSegmentsFromEntryNode(used_segs[0]['from'], routes_by_entry_node))
    next_allowed_segs = getUniqueElements(next_allowed_segs)
    if len(next_allowed_segs) == 0:
        return []
    elif len(next_allowed_segs) == 1:
        used_segs.append(next_allowed_segs[0])
        return find_forbidden_seq(next_allowed_segs[0], used_segs, allowed_segments, routes_by_entry_node)
    else: # we have multiple segments to chose as next
        # find splitted route from the current path that have merged again
        forbidden_tmp = []
        for sg in next_allowed_segs:
            for route in routes_by_entry_node[used_segs[0]['from']]:
                if not(issubset(used_segs, route)) and any([s['to']==node for s in route]) and sg not in route: # if splitted and merged and (forbidden sg?)
                    route_used_segs = list(reversed(getUsedSegsBeforeNode(node, route)))
                    # try all possible forbid seq of length 2 and check if any route from current entry_node gets violated
                    # if not, we set seq as a forbid_seq
                    for i in range(len(route_used_segs)):
                        seq = [route_used_segs[i], sg]
                        if not(any([issubset(seq, r) for r in routes_by_entry_node[used_segs[0]['from']]])):
                            if seq not in forbidden_tmp:
                                forbidden_tmp.append(seq)
                                break

            used_segs_tmp = list(used_segs)
            used_segs_tmp.append(sg)
            forbidden_tmp_more = find_forbidden_seq(sg, used_segs_tmp, allowed_segments, routes_by_entry_node)
            if forbidden_tmp_more:
                for forbid in forbidden_tmp_more:
                    forbidden_tmp.append(forbid)
        
        return forbidden_tmp

def getForbiddenSequences(routes_by_entry_node, segments, allowed_routes, allowed_segments):
    forbidden_seqs = {}
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
        last_seg = {}
        for seg in possible_segs:
            tmp_seg = {'airway': seg['airway'], 'from': seg['to'], 'to': seg['from']}
            if (seg not in used_segs) and (seg not in forbidden_tmp) and (tmp_seg != last_seg):
                forbidden_tmp.append(seg)
            last_seg = seg

        #Find which sequences to forbid (prevent routes from splitting and merge and then splitting again)
        for entry_seg in getAllowedSegmentsFrom(entry_node, getAllowedSegmentsFromEntryNode(entry_node, routes_by_entry_node)):
            forbidden_tmp.extend(find_forbidden_seq(entry_seg, [entry_seg], allowed_segments, routes_by_entry_node))
        forbidden_tmp = getUniqueElements(forbidden_tmp)

        forbidden_seqs[entry_node] = forbidden_tmp

    return forbidden_seqs

def getSegmentsTo(to, segments):
        segs = [seg for seg in segments if seg['to']==to]
        return segs

def getSegmentsFrom(fr, segments):
        segs = [seg for seg in segments if seg['from']==fr]
        return segs

def getForbiddenEntrySegments(allowed_segments, segments, chinese_areas, entry_nodes, allowed_nodes):
    forbidden_entry_segs = []

    # Find all segments that goes in to China from another country that doesn't use an entry_node or an allowed route
    for seg in segments:
        fr = seg['from'][-2:]
        to = seg['to'][-2:]
        if     (fr not in chinese_areas) \
           and (to in chinese_areas) \
           and (seg not in allowed_segments) \
           and (seg['to'] not in entry_nodes):
            forbidden_entry_segs.append(seg)

    # if there are more than just the entry_node outside of China, forbid segments that allowes us to hop on after the entry_node
    for node in allowed_nodes:
        if node[-2:] not in chinese_areas and node not in entry_nodes:
            for seg in getSegmentsTo(node, segments):
                if seg not in allowed_segments:
                    forbidden_entry_segs.append(seg)

    return forbidden_entry_segs
