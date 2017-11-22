#Program to create forbid segments
#The program checks all mandatory routes, grouped by entry point to China, and 
#finds the set of segments that need to be forbidden so that only the mandatory
#routes are possible to choose. 
def readFile(path):
    with open(path,'r') as f:
        return f.read()

def getForbiddenSequences(routes_by_entry_node, segments, allowed_routes):
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

def getForbiddenEntrySegments(allowed_segments, segments):
    forbidden_entry_segs = []

    for seg in segments:
        fr = seg['from'][-2]
        to = seg['to'][-2]
        if (fr != 'Z' and to == 'Z') and (seg not in allowed_segments): # if seg is from another country to China
            forbidden_entry_segs.append(seg)

    return forbidden_entry_segs


