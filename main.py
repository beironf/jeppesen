import parse_data
import create_forbid_sequences
import generate_srad
from confirm_solution import ConfirmSolution
import plot_routes
import pprint
import splitted_routes_that_merge

pp = pprint.PrettyPrinter(indent = 4)

# import variables
segments = parse_data.getSegments()
possible_destinations = parse_data.getPossibleDestinations(segments)
allowed_routes = parse_data.getAllowedRoutes(segments)
points = parse_data.getPoints()
routes_by_entry_node = parse_data.getRoutesForAllEntryNodes(allowed_routes)
overflyRules = parse_data.getOverflyRules()
entry_nodes = list(routes_by_entry_node.keys())
exit_nodes = parse_data.getExitNodes(allowed_routes)



allowed_nodes = parse_data.getAllowedNodes(allowed_routes)

pp.pprint(points['WPT ASURI'])


# generate forbidden constraints
forbidden_seqs = create_forbid_sequences.getForbiddenSequences(routes_by_entry_node, segments, allowed_routes)
#forbidden_entry_segs = create_forbid_segments.getForbiddenEntrySegments(routes_by_entry_node, entry_nodes, segments, points)


# generate .srad-file
generate_srad.generateSRAD(overflyRules, [], forbidden_seqs, points)
# confirm solution
cs = ConfirmSolution(forbidden_seqs, [], segments, points, entry_nodes, exit_nodes, allowed_nodes)
possible_routes = cs.getPossibleRoutes()
#pp.pprint(possible_routes[0][0])


SRTM = splitted_routes_that_merge.getSplittedRoutesThatMerge(possible_routes)

pp.pprint(SRTM)




#pp.pprint(possible_routes[4])
#pp.pprint(len(possible_routes))


pp.pprint(possible_destinations['WPT MAGOG'])

# plot routes
plot_routes.plotRoutes(allowed_routes, possible_routes, points, segments, entry_nodes)

#pp.pprint(forbidden_segs['WPT SADLI'])