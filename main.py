import parse_data
import create_forbid_sequences
import generate_srad
from confirm_solution import ConfirmSolution
import plot_routes
import pprint
import splitted_routes_that_merge

pp = pprint.PrettyPrinter(indent = 4)

# import variables
print('Get segments')
segments = parse_data.getSegments()
print('Get possible destinations')
possible_destinations = parse_data.getPossibleDestinations(segments)
print('Get allowed routes')
allowed_routes = parse_data.getAllowedRoutes(segments)
print('Get all points')
points = parse_data.getPoints()
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
forbidden_entry_segs = create_forbid_sequences.getForbiddenEntrySegments(allowed_segments, segments, points)


# generate .srad-file
print('Generate new srad file')
generate_srad.generateSRAD(overflyRules, [], forbidden_seqs, points)
# confirm solution
print('Confirm if correct solutions')
cs = ConfirmSolution(forbidden_seqs, [], segments, points, entry_nodes, exit_nodes, allowed_nodes)
possible_routes = cs.getPossibleRoutes()
#pp.pprint(possible_routes[0][0])

print('Find if any routes split and then merge again')
SRTM = splitted_routes_that_merge.getSplittedRoutesThatMerge(possible_routes)

pp.pprint(SRTM)

#pp.pprint(possible_routes[4])
print('The number of routes found is ', len(possible_routes))

# plot routes
print('Saving figures:')
plot_routes.plotRoutes(allowed_routes, possible_routes, points, segments, entry_nodes)

