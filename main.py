import parse_data
import create_forbid_segments
import generate_srad
from confirm_solution import ConfirmSolution

# import variables
segments = parse_data.getSegments()
possible_destinations = parse_data.getPossibleDestinations(segments)
allowed_routes = parse_data.getAllowedRoutes()
points = parse_data.getPoints(segments)
routes_by_entry_node = parse_data.getRoutesForAllEntryNodes(allowed_routes)
overflyRules = parse_data.getOverflyRules()
entry_nodes = routes_by_entry_node.keys()

# generate forbidden constraints
forbidden_segs = create_forbid_segments.getForbiddenSegments(routes_by_entry_node, segments)
forbidden_entry_segs = create_forbid_segments.getForbiddenEntrySegments(routes_by_entry_node, entry_nodes, segments, points)

# generate .srad-file
generate_srad.generateSRAD(overflyRules, forbidden_entry_segs, forbidden_segs, points)

# confirm solution
#cs = ConfirmSolution(forbidden_segs, forbidden_entry_segs, segments, points, entry_nodes, possible_destinations)
#possible_routes = cs.getPossibleRoutes()
#print(possible_routes[0])
#print(len(possible_routes))

tuples = [(seg['from'], seg['to']) for seg in segments]
print(len(tuples))
tuples = list(set(tuples))
print(len(tuples))
