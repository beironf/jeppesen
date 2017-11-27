import parse_data
import create_forbid_sequences
import generate_srad
from confirm_solution import ConfirmSolution
import plot_routes
import pprint
import splitted_routes_that_merge

pp = pprint.PrettyPrinter(indent = 4)

chinese_areas = ['ZB',
                 'ZG',
                 'ZH',
                 'ZL',
                 'ZP',
                 'ZS',
                 'ZW',
                 'ZY']

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
print('Get list with all segments in allowed routes')
allowed_segments = parse_data.getAllowedSegments(allowed_routes)

print('Create list of forbidden segments and sequences')
forbidden_seqs = create_forbid_sequences.getForbiddenSequences(routes_by_entry_node, segments, allowed_routes, allowed_segments)
forbidden_entry_segs = create_forbid_sequences.getForbiddenEntrySegments(allowed_segments, segments, chinese_areas, entry_nodes, allowed_nodes)

print('Generate new srad file')
generate_srad.generateSRAD_f(overflyRules, forbidden_entry_segs, forbidden_seqs, points)
generate_srad.generateSRAD_m(overflyRules, forbidden_entry_segs, forbidden_seqs, points)

print('Confirm solution')
cs = ConfirmSolution(forbidden_seqs, [], segments, points, entry_nodes, exit_nodes, allowed_nodes, chinese_areas)
possible_routes = cs.getPossibleRoutes()

print('\nNr of routes per entry node\n')
nr_of_routes_per_entry = {}
for entry_node in entry_nodes:
    count_allowed = 0
    count_possible = 0
    for route in allowed_routes:
        if route[0]['from'] == entry_node:
            count_allowed = count_allowed+1
    for route in possible_routes:
        if route[0]['from'] == entry_node:
            count_possible = count_possible+1
    nr_of_routes_per_entry[entry_node] = {'allowed': count_allowed, 'possible': count_possible}
pp.pprint(nr_of_routes_per_entry)

print('\nNr of routes:')
count_identical = 0
for pr in possible_routes:
    for ar in allowed_routes:
        if pr == ar:
            count_identical = count_identical + 1
print('The number of routes found is ', len(possible_routes))
print('The number of identical routes ', count_identical) 

print('Saving figures')
plot_routes.plotRoutes(allowed_routes, possible_routes, points, segments, entry_nodes, chinese_areas)


