# Program to parse data from NAVDATA_POINTS, NAVDATA_SEGMENTS and the
# .srad-file from Jeppesen

from graph import Graph

mapping = {"1": "W",
           "2": "V",
           "3": "N",
           "4": "D",
           "5": "A",
           "6": "R"}

#Read all segments from file
segmentSource = open("../data/NAVDATA_SEGMENTS", 'r')
segmentlist = segmentSource.readlines()
segmentSource.close()

#Create list of segment tuples, becoming edges in our graph
segments = []
for line in segmentlist:
    if line[15]=="Z" or line[29]=="Z":
        seg = (line[9:14].strip(), line[23:28].strip())
        seg = (seg[0]+" "+mapping[line[21]], seg[1]+" "+mapping[line[35]])
        segments.append(seg)

#create the graph
g=Graph(segments, directed=True)
#print(g._graph)
#print(g._graph['IDUMA'])

#Read in allowed paths from .srad file
sradfile = open("../data/_CHINA_MANDATE_OVERFLIGHT.srad", 'r')
srad = sradfile.readlines()
sradfile.close()

#Find the index of all mandate routes sequences in the code
index = [];
for i,line in enumerate(srad):
    if "Seq" in line:
        index.append(i)

#Get every allowed route
allowed_routes = []
for i,ind in enumerate(index):
    allowed_routes.append([])
    if ind != index[-1]:
        for line in srad[ind+1:index[i+1]]:
            node = line.split()
            seg = (node[9]+" "+node[8][0], node[13]+" "+node[12][0])
            allowed_routes[i].append(seg)
    else:
        for line in srad[ind+1:len(srad)]:
            node = line.split()
            seg = (node[9]+" "+node[8][0], node[13]+" "+node[12][0])
            allowed_routes[i].append(seg)

print(allowed_routes)

