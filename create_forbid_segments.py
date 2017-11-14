# Program to create forbid segments

import parse_data

graph = parse_data.createGraph()
allowed_routes = parse_data.getAllowedRoutes()
entry_nodes = parse_data.getEntryNodes(allowed_routes)

for entry_node in entry_nodes:
    #Create list with all routes originating in entry_node
    current_routes = []
    for route in allowed_routes:
        if route[0][0] == entry_node:
            #We are now looking at a route with 'node' as its starting node
            current_routes.append(route)
    #Now current_routes contains several lists, each with a route from
    #entry_node

