import numpy as np
import matplotlib.pyplot as plt

def plotRoutes(allowed_routes, possible_routes, points, segments, entry_nodes):

    china_points = [p for p in points if points[p]['area'][0]=='Z']
    china_lat = [points[p]['lat'] for p in china_points]
    china_lon = [points[p]['lon'] for p in china_points]
    
    edge_x = []
    edge_y = []
    for i in [10, 16, 3, 17, 0, 8, 20]:
        edge_x.append(points[entry_nodes[i]]['lon'])
        edge_y.append(points[entry_nodes[i]]['lat'])

    # Create list of allowed routes for all entry_nodes containing [lon, lat] from -> to
    allowed_segs = []
    for entry_node in entry_nodes:
        tmp_routes = []
        for route in allowed_routes:
            tmp_segs = []
            if route[0]['from'] == entry_node:
                for seg in route:
                    tmp_segs.append([[points[seg['from']]['lon'], points[seg['from']]['lat']], [points[seg['to']]['lon'], points[seg['to']]['lat']]])
                tmp_routes.append(tmp_segs)
        allowed_segs.append(tmp_routes)

    # Create list of possible routes for all entry_nodes containing [lon, lat] from -> to
    possible_segs = []
    for entry_node in entry_nodes:
        tmp_routes = []
        for route in possible_routes:
            tmp_segs = []
            if route[0]['from'] == entry_node:
                for seg in route:
                    tmp_segs.append([[points[seg['from']]['lon'], points[seg['from']]['lat']], [points[seg['to']]['lon'], points[seg['to']]['lat']]])
                tmp_routes.append(tmp_segs)
        possible_segs.append(tmp_routes)

    # Convert to list of routes for each entry_node with lon (x) and lat (y) variables for allowed (a)
    a_x = []
    a_y = []
    for a_segs in allowed_segs:
        tmp_entry_x = []
        tmp_entry_y = []
        for route in a_segs:
            tmp_route_x = [route[0][0][0]]
            tmp_route_y = [route[0][0][1]]
            for seg in route:
                tmp_route_x.append(seg[1][0])
                tmp_route_y.append(seg[1][1])
            tmp_entry_x.append(tmp_route_x)
            tmp_entry_y.append(tmp_route_y)
        a_x.append(tmp_entry_x)
        a_y.append(tmp_entry_y)

    # Convert to list of routes for each entry_node with lon (x) and lat (y) variables for possible (p)
    p_x = []
    p_y = []
    for p_segs in possible_segs:
        tmp_entry_x = []
        tmp_entry_y = []
        for route in p_segs:
            tmp_route_x = [route[0][0][0]]
            tmp_route_y = [route[0][0][1]]
            for seg in route:
                tmp_route_x.append(seg[1][0])
                tmp_route_y.append(seg[1][1])
            tmp_entry_x.append(tmp_route_x)
            tmp_entry_y.append(tmp_route_y)
        p_x.append(tmp_entry_x)
        p_y.append(tmp_entry_y)



    # Print out the routes
    fig1, axes1 = plt.subplots(4, 4, sharex=True, sharey=True)
    for i in range(4):
        for j in range(4):
            ind = i*4+j
            axes1[i,j].scatter(china_lon, china_lat, c=(0.8,0.8,0.8), s=2)
            axes1[i,j].plot(edge_x, edge_y, color=(0.3,0.3,0.3), linewidth=1)
            axes1[i,j].plot(allowed_segs[ind][0][0][0][0], allowed_segs[ind][0][0][0][1], 'bo', markersize=6)
            for k in range(len(a_x[ind])):
                axes1[i,j].plot(a_x[ind][k], a_y[ind][k], 'g-', linewidth=3)
            for k in range(len(p_x[ind])):
                axes1[i,j].plot(p_x[ind][k], p_y[ind][k], 'r-', linewidth=0.8)
            axes1[i,j].set_aspect('equal')

    fig2, axes2 = plt.subplots(3, 4, sharex=True, sharey=True)
    for i in range(3):
        for j in range(4):
            ind = 15+i*4+j
            axes2[i,j].scatter(china_lon, china_lat, c=(0.8,0.8,0.8), s=5)
            axes2[i,j].plot(edge_x, edge_y, color=(0.3,0.3,0.3), linewidth=1)
            axes2[i,j].plot(allowed_segs[ind][0][0][0][0], allowed_segs[ind][0][0][0][1], 'bo', markersize=8)
            for k in range(len(a_x[ind])):
                axes2[i,j].plot(a_x[ind][k], a_y[ind][k], 'g-', linewidth=4)
            for k in range(len(p_x[ind])):
                axes2[i,j].plot(p_x[ind][k], p_y[ind][k], 'r-', linewidth=1)
            axes2[i,j].set_aspect('equal')

    plt.tight_layout()
    plt.show()

