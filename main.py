import parse_data
import create_forbid_segments
import generate_srad

# import variables
segments = parse_data.getSegments()
possible_destinations = parse_data.getPossibleDestinations(segments)
allowed_routes = parse_data.getAllowedRoutes()
points = parse_data.getPoints(segments)
routes_by_entry_node = parse_data.getRoutesForAllEntryNodes(allowed_routes)
overflyRules = parse_data.getOverflyRules()


# generate forbidden constraints
forbidden_segs = create_forbid_segments.getForbiddenSegments(routes_by_entry_node, segments)
forbidden_entry_segs = create_forbid_segments.getForbiddenEntrySegments(routes_by_entry_node, segments, points)

# generate .srad-file
generate_srad.generateSRAD(overflyRules, forbidden_entry_segs, forbidden_segs, points)
