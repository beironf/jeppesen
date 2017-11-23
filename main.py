import parse_data
import create_forbid_sequences
import generate_srad
from confirm_solution import ConfirmSolution
import plot_routes
import pprint
import splitted_routes_that_merge

pp = pprint.PrettyPrinter(indent = 4)

# import variables
print('Get all points')
points = parse_data.getPoints()
print('Get segments')
segments = parse_data.getSegments(points)
print('Get possible destinations')
possible_destinations = parse_data.getPossibleDestinations(segments)
print('Get allowed routes')
allowed_routes = parse_data.getAllowedRoutes(segments)
print('Sort all routes by entry node')
routes_by_entry_node = parse_data.getRoutesForAllEntryNodes(allowed_routes)
print('Read rules for overflight from srad file')
overflyRules = parse_data.getOverflyRules()
print('Make a list of all entry nodes')
entry_nodes = list(routes_by_entry_node.keys())
print('Get all exit nodes')
exit_nodes = parse_data.getExitNodes(allowed_routes)
print('Find all allowed nodes from the allowed routes list')
allowed_nodes = parse_data.getAllowedNodes(allowed_routes)
print('Get list with all segments in alowed routes')
allowed_segments = parse_data.getAllowedSegments(allowed_routes)

# generate forbidden constraints
print('Create list of forbidden segments')
forbidden_seqs = create_forbid_sequences.getForbiddenSequences(routes_by_entry_node, segments, allowed_routes)
forbidden_entry_segs = create_forbid_sequences.getForbiddenEntrySegments(allowed_segments, segments)
#pp.pprint(forbidden_seqs)

# generate .srad-file
print('Generate new srad file')
generate_srad.generateSRAD(overflyRules, forbidden_entry_segs, forbidden_seqs, points)

# confirm solution
print('Confirm if correct solutions')
cs = ConfirmSolution(forbidden_seqs, [], segments, points, entry_nodes, exit_nodes, allowed_nodes)
possible_routes = cs.getPossibleRoutes()

print('Find if any routes split and then merge again')
SRTM = splitted_routes_that_merge.getSplittedRoutesThatMerge(possible_routes)


#for i in range(0, len(possible_routes)):
 #   pp.pprint(str(i) + " " + possible_routes[i][0]['from'])

#splitted_routes_that_merge.splittedRoutesThatMerge(possible_routes[10], possible_routes[16])

#pp.pprint(possible_routes[4])
print('The number of routes found is ', len(possible_routes))

# plot routes




print('Saving figures:')
plot_routes.plotRoutes(allowed_routes, possible_routes, points, segments, entry_nodes)
count = 0
not_in_allowed = []
not_in_possible = []
for j,pr in enumerate(possible_routes):
    bool_temp = False
    for i,ar in enumerate(allowed_routes):
        if pr == ar:
            count = count + 1
            #pp.pprint(j)
            #pp.pprint(i)
            #pp.pprint(" ")
            bool_temp = True
    if bool_temp == False:
        not_in_allowed.append(pr)        


for j,ar in enumerate(allowed_routes):
    bool_temp = False 
    for i,pr in enumerate(possible_routes):
        if ar == pr:
            bool_temp = True
    if bool_temp == False:
        not_in_possible.append(ar)

pp.pprint(SRTM)


