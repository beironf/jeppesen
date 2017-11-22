

def splittedRoutesThatMerge(route1, route2):
    hasSplitted = False
    hasMerged = False
    if (len(route1) > len(route2)):
        route1_tmp = route1
        route1 = route2
        route2 = route1_tmp

    for i in range(0, len(route1)):
        if (hasSplitted == False and hasMerged == False and route1[i] != route2[i]):
            hasSplitted = True
            splitNode = i

        elif (hasMerged == False and hasSplitted):
            for j in range(splitNode, len(route2)):
                if (route1[i] == route2[j]):
                    hasMerged = True
                    mergeNode = j

        elif (hasMerged and hasSplitted):
            for j in range(mergeNode, len(route1)):
                if (route1[i] != route2[j]):
                    return True
        else:
            return False

def getSplittedRoutesThatMerge(routes):
    splitted_routes_that_merge = 0
    for i in range(0, len(routes)-1):
        for j in range(1, len(routes)):
            if (splittedRoutesThatMerge(routes[i], routes[j])):
                splitted_routes_that_merge = splitted_routes_that_merge + 1
                

    return splitted_routes_that_merge
                


