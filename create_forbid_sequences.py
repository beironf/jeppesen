#Program to create forbid segments and sequences
#The program checks all mandatory routes, grouped by entry point to China, and 
#finds the set of segments and sequences that need to be forbidden so that only the mandatory
#routes are possible to choose. 
def readFile(path):
    with open(path,'r') as f:
        return f.read()

def getForbiddenSequences2(routes_by_entry_node, segments, allowed_routes):
    srtm_lines = readFile('SRTM.txt')
    srtm_lines = [seq.replace(']','').replace(',\n','').strip() for seq in srtm_lines.split('[')][1:]
    srtm = []
    srtm_entry = []
    for seq in srtm_lines:
        tmp_list = seq.split('    ')
        tmp_seq = []
        
        for i,l in (enumerate(tmp_list)):
            if i == 0:
                node = l.split(': ')
                srtm_entry.append(node[2][1:-7]) 
            else:
                node = l.split(': ')
                seg_tmp = {'airway': node[1][1:-9], 'from': node[2][1:-7], 'to': node[3][1:-2]}
                tmp_seq.append(seg_tmp)
        srtm.append(tmp_seq)
    #forbidden_seqs = srtm
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
        for seg in possible_segs:
            if (seg not in used_segs) and (seg not in forbidden_tmp):
                forbidden_tmp.append(seg)

        for i,entry_point in enumerate(srtm_entry):
            if entry_point == entry_node:
                forbidden_tmp.append(srtm[i])

        forbidden_seqs[entry_node] = forbidden_tmp

    return forbidden_seqs

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
                    route_used_segs = getUsedSegsBeforeNode(node, route)
                    # create all possible forbid seq and check if any route from current entry_node gets violated
                    # if not, we set seq as a forbid_seq
                    for i in range(len(route_used_segs)-1):
                        seq = [route_used_segs[i], route_used_segs[i+1], sg]
                        if not(any([issubset(seq, r) for r in routes_by_entry_node[used_segs[0]['from']]])):
                            if seq not in forbidden_tmp:
                                forbidden_tmp.append(seq)

                    #print("\nEntry_node: "+used_segs[0]['from']+"\n Couldn't forbid "+str(sg)+" for seq:\n\n"+str(route_used_segs+[sg]))

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
        for seg in possible_segs:
            if (seg not in used_segs) and (seg not in forbidden_tmp):
                forbidden_tmp.append(seg)

        #Find which sequences to forbid (prevent routes from splitting and merge and then splitting again)
        for entry_seg in getAllowedSegmentsFrom(entry_node, getAllowedSegmentsFromEntryNode(entry_node, routes_by_entry_node)):
            forbidden_tmp.extend(find_forbidden_seq(entry_seg, [entry_seg], allowed_segments, routes_by_entry_node))
        forbidden_tmp = getUniqueElements(forbidden_tmp)

        forbidden_seqs[entry_node] = forbidden_tmp

    return forbidden_seqs

def getForbiddenEntrySegments(allowed_segments, segments, chinese_areas, entry_nodes):
    forbidden_entry_segs = []

    for seg in segments:
        fr = seg['from'][-2:]
        to = seg['to'][-2:]
        if fr not in chinese_areas \
            and to in chinese_areas \
            and (seg not in allowed_segments) \
            and (seg['to'] not in entry_nodes): # if seg is from another country to China
            forbidden_entry_segs.append(seg)

    return forbidden_entry_segs


