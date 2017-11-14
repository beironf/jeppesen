from graph import Graph

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

def readFileLines(path):
    with open(path,'r') as f:
        return f.readlines()
    
def readFile(path):
    with open(path,'r') as f:
        return f.read()

#------------------------------------------------#
#      Create list of all segments in China      #
#------------------------------------------------#
def getSegments():
    segment_lines = readFileLines(segment_path)
    segments = []
    for line in segment_lines:
        if line[15]=="Z" or line[29]=="Z":  # pick the segments with at least one node in China ("z")
            segments.append({
                'airway': 'AWY '+line[2:8].strip(),
                'from': mapping[line[21]]+" "+line[9:14].strip(), 
                'to': mapping[line[35]]+" "+line[23:28].strip()
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
def getAllowedRoutes():
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
        allowed_routes.append(tmp_seq)
    return allowed_routes
    
#--------------------------------------------------------#
#      Create a dictionary with all points in China      #
#--------------------------------------------------------#
def getPoints(segments):
    # import from file
    pointlines = readFileLines(point_path)
    points = {}
    for line in pointlines:
        points[pointType[line[0]]+" "+line[2:7].strip()] = {
            'area': line[19:23], 
            'lat': line[34:40].strip(), 
            'lon': line[41:48]
        }
    # create a dictionary with all points in China from our segments
    china_points = []
    for seg in segments:
        china_points.extend([seg['from'],seg['to']])
    china_points = list(set(china_points))
    # delete all points that are not in China
    points_all = dict(points)
    for p in points_all:
        if p not in china_points:
            del points[p]
    return points

def getEntryNodes():
    entry_nodes = []
    for route in allowed_routes:
        if not(route[0]['from'] in entry_nodes):
            entry_nodes.append(route[0]['from'])
        
    for entry_node in entry_nodes:
        current_routes = []
        for route in allowed_routes:
            if route[0]['from'] == entry_node:
                current_routes.append(route)
                
        for route in current_routes:
            for node in allowed_routes:
    return entry_nodes