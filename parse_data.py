from graph import Graph
from decimal import Decimal

point_path = "../data/NAVDATA_POINTS"
segment_path = "../data/NAVDATA_SEGMENTS"
srad_path = "../data/_CHINA_MANDATE_OVERFLIGHT.srad"

mapping = {"1": "WPT",
           "2": "VOR",
           "3": "NDB",
           "4": "DME",
           "5": "APT",
           "6": "RWY"}

pointType = {'V': 'VOR',
             'W': 'WPT',
             'N': 'NDB',
             'A': 'APT',
             'D': 'DME',
             'R': 'RWY'}

def convertCoord(coord):
    direction, value = coord[0], coord[1:]
    retval = Decimal(value[:-3]) + Decimal(value[-3:])/Decimal('600')
    if direction in ('S', 'W'):
        retval = -retval
    retval = '%.3f'%(retval) # convert to 3-decimals and string
    return retval

def readFileLines(path):
    with open(path,'r') as f:
        return f.readlines()
    
def readFile(path):
    with open(path,'r') as f:
        return f.read()

def getOverflyRules():
    sourcelines = readFileLines(srad_path)
    return sourcelines[2:31]


#------------------------------------------------#
#      Create list of all segments in China      #
#------------------------------------------------#
def getSegments(points):
    segment_lines = readFileLines(segment_path)
    segments = []
    for line in segment_lines:
        fr = mapping[line[21]]+" "+line[9:14].strip()+" "+line[15:17]
        to = mapping[line[35]]+" "+line[23:28].strip()+" "+line[29:31]
        if fr in points.keys() and to in points.keys():
            fr_co = [float(points[fr]['lon']), float(points[fr]['lat'])]
            to_co = [float(points[to]['lon']), float(points[to]['lat'])]
            if (fr_co[0]>60 and fr_co[0]<150 and fr_co[1]>0 and fr_co[1]<70) or (to_co[0]>60 and to_co[0]<150 and to_co[1]>0 and to_co[1]<70):
                segments.append({
                    'airway': 'AWY '+line[2:8].strip(),
                    'from': fr,
                    'to': to
                })
    return segments
        
#---------------------------------------------------------------------------#
#      Create dictionary with all possible destinations for each point      #
#---------------------------------------------------------------------------#
def getPossibleDestinations(segments):
    tuples = [(seg['from'], seg['to']) for seg in segments]
    possible_destinations = Graph(tuples, directed=True)._graph
    return possible_destinations

#-------------------------------------------------#
#      Create a list with all allowed routes      #
#-------------------------------------------------#
def getAllowedRoutes(segments):
    # import from file
    allowed_routes = []
    sequences = readFile(srad_path)
    # Clean input:   | indentation     | ")) " before next "(Seq"                              | the first ~30 rows
    sequences = [seq.replace('   ','').replace(')) ',')') for seq in sequences.split('(Seq\n')][1:]
    sequences = [seq.split('\n')[:-1] for seq in sequences]  # remove empty "" element from each sequence
    for seq in sequences:
        tmp_seq = []
        for seg in seq:
            cols = seg.split(' ')
            tmp_seq.append({
                'airway': cols[6]+" "+cols[7],
                'from': cols[8]+" "+cols[9],
                'to': cols[12]+" "+cols[13]
            })

        #Find corresponding segment in the segment list to
        #get correct point type
        tmp_seq2 = []
        for tmp_seg in tmp_seq:
            for seg in segments:
                if tmp_seg['airway']==seg['airway'] and \
                    tmp_seg['from'] in seg['from'] and \
                    tmp_seg['to'] in seg['to']:
                    tmp_seq2.append(seg)

        allowed_routes.append(tmp_seq2)
    return allowed_routes

#-------------------------------------------------#
#      Create a list with all allowed segments    #
#-------------------------------------------------#
def getAllowedSegments(allowed_routes):
    allowed_segments = []
    for route in allowed_routes:
        for seg in route:
            if seg not in allowed_segments:
                allowed_segments.append(seg)
    return allowed_segments

#------------------------------------------------#
#      Create a list with all allowed nodes      #
#------------------------------------------------#
def getAllowedNodes(allowed_routes):
    allowed_nodes = []
    for route in allowed_routes:
        for seg in route:
            allowed_nodes.extend([seg['from'], seg['to']])
    allowed_nodes = list(set(allowed_nodes))
    return allowed_nodes
    
#--------------------------------------------------------#
#      Create a dictionary with all points in China      #
#--------------------------------------------------------#
def getPoints():
    # import from file
    pointlines = readFileLines(point_path)
    points = {}
    for line in pointlines:
        if line[8:10] != "  ":
            points[pointType[line[0]]+" "+line[2:7].strip()+" "+line[8:10]] = {
                'area': line[19:23], 
                'lat': convertCoord(line[34:40]), 
                'lon': convertCoord(line[41:48])
            }
        else:
            points[pointType[line[0]]+" "+line[2:7].strip()+" xx"] = {
                'area': line[19:23], 
                'lat': convertCoord(line[34:40]), 
                'lon': convertCoord(line[41:48])
            }

    return points

#-------------------------------------------------------------------#
#      Create a dictionary with all routes for each entry node      #
#-------------------------------------------------------------------#
def getRoutesForAllEntryNodes(allowed_routes):
    entry_nodes = []
    for route in allowed_routes:
        if not(route[0]['from'] in entry_nodes):
            entry_nodes.append(route[0]['from'])
    
    routes_for_entry_node = {}
    for entry_node in entry_nodes:
        current_routes = []
        for route in allowed_routes:
            if route[0]['from'] == entry_node:
                current_routes.append(route)
        routes_for_entry_node[entry_node] = current_routes
        
    return routes_for_entry_node

def getExitNodes(allowed_routes):
    exit_nodes = []
    for route in allowed_routes:
        
        if not(route[len(route)-1]['to'] in exit_nodes):
            exit_nodes.append(route[len(route)-1]['to'])
    return exit_nodes
